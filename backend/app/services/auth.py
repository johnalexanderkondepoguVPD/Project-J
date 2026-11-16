import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from passlib.context import CryptContext

from app.Models.session import Session
from app.Models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.exceptions import AuthenticationException, ValidationException
from app.database import SessionLocal


pwd_context = CryptContext(schemes=["argon2"], default="argon2")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


class AuthService:
    """Server-side session-based authentication service."""

    def _get_db(self):
        """Get a database session."""
        return SessionLocal()

    def register(self, user_data: UserCreate) -> UserResponse:
        """Register a new user with session creation."""
        db = self._get_db()
        try:
            # Check if user already exists
            from sqlalchemy import select
            stmt = select(User).where(User.email == user_data.email)
            result = db.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise ValidationException(detail="Email already registered")

            stmt = select(User).where(User.username == user_data.username)
            result = db.execute(stmt)
            existing_username = result.scalar_one_or_none()

            if existing_username:
                raise ValidationException(detail="Username already taken")

            # Create user with hashed password
            hashed_password = get_password_hash(user_data.password)
            user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
            )
            db.add(user)
            db.flush()

            # Create initial session for the user
            session_id = secrets.token_hex(32)  # 256-bit cryptographically secure random
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)

            session = Session(
                session_hash=session_hash,
                user_id=user.id,
                expires_at=expires_at,
            )
            db.add(session)
            db.flush()
            db.commit()

            return UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
            )
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def login(self, login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate user and create session."""
        db = self._get_db()
        try:
            # Try to find user by email or username
            from sqlalchemy import select
            stmt = select(User).where(
                (User.email == login_data.identifier) | (User.username == login_data.identifier)
            )
            result = db.execute(stmt)
            user = result.scalar_one_or_none()

            if not user or not verify_password(login_data.password, user.hashed_password):
                raise AuthenticationException(detail="Invalid credentials")

            if not user.is_active:
                raise AuthenticationException(detail="User account is disabled")

            # Create session
            session_id = secrets.token_hex(32)  # 256-bit CSRF-safe
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)

            session = Session(
                session_hash=session_hash,
                user_id=user.id,
                expires_at=expires_at,
            )
            db.add(session)
            db.flush()
            db.commit()

            return {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                },
                "session_id": session_id,
            }
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def logout(self, session_id: str) -> bool:
        """Revoke a session and clear the cookie."""
        db = self._get_db()
        try:
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()

            from sqlalchemy import select as sa_select
            stmt = sa_select(Session).where(Session.session_hash == session_hash)
            result = db.execute(stmt)
            session = result.scalar_one_or_none()

            if session:
                session.revoked = True
                db.flush()
                db.commit()
                return True

            return False
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_current_user(self, session_id: str) -> Optional[UserResponse]:
        """Get the authenticated user for a given session ID."""
        db = self._get_db()
        try:
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()

            from sqlalchemy import select as sa_select
            stmt = sa_select(Session).where(
                Session.session_hash == session_hash,
                Session.revoked == False,
            )
            result = db.execute(stmt)
            session = result.scalar_one_or_none()

            if not session:
                return None

            # Check expiry
            if session.expires_at < datetime.now(timezone.utc):
                return None

            # Get the associated user
            stmt = sa_select(User).where(User.id == session.user_id)
            result = db.execute(stmt)
            user = result.scalar_one_or_none()

            if not user or not user.is_active:
                return None

            return UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
            )
        except Exception:
            raise
        finally:
            db.close()