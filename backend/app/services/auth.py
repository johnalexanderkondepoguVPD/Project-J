import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from passlib.context import CryptContext
from sqlalchemy import select

from app.Models.session import Session
from app.Models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.config import settings
from app.database import SessionLocal


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], default="argon2")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


class AuthService:
    """Server-side session-based authentication service."""

    def __init__(self, db_session=None):
        self._custom_db = db_session

    def _get_db(self):
        """Get a database session."""
        if self._custom_db is not None:
            return self._custom_db
        return SessionLocal()

    def _close_db_if_local(self, db):
        """Close DB session only if it was created locally."""
        if self._custom_db is None:
            db.close()

    def register(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user and create an initial session."""
        db = self._get_db()
        try:
            # Check if email is already registered
            stmt = select(User).where(User.email == user_data.email)
            result = db.execute(stmt)
            if result.scalar_one_or_none():
                raise ValidationException(detail="Email already registered")

            # Check if username is already taken
            stmt = select(User).where(User.username == user_data.username)
            result = db.execute(stmt)
            if result.scalar_one_or_none():
                raise ValidationException(detail="Username already taken")

            # Create user with hashed password
            hashed_password = get_password_hash(user_data.password)
            user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
                is_active=True,
                is_verified=False,
            )
            db.add(user)
            db.flush()

            # Create initial session for the registered user
            session_id = secrets.token_hex(32)  # 256-bit cryptographically secure random
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()
            expires_at = datetime.now(timezone.utc) + timedelta(days=settings.session_expire_days)

            session = Session(
                session_hash=session_hash,
                user_id=user.id,
                expires_at=expires_at,
            )
            db.add(session)
            db.flush()
            db.commit()
            db.refresh(user)

            user_resp = UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
            )

            return {
                "user": user_resp,
                "session_id": session_id,
            }
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)

    def login(self, login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate user and create session."""
        db = self._get_db()
        try:
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
            session_id = secrets.token_hex(32)
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()
            expires_at = datetime.now(timezone.utc) + timedelta(days=settings.session_expire_days)

            session = Session(
                session_hash=session_hash,
                user_id=user.id,
                expires_at=expires_at,
            )
            db.add(session)
            db.flush()
            db.commit()
            db.refresh(user)

            user_resp = UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
            )

            return {
                "user": user_resp,
                "session_id": session_id,
            }
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)

    def logout(self, session_id: str) -> bool:
        """Revoke a session and mark it revoked."""
        if not session_id:
            return False
        db = self._get_db()
        try:
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()

            stmt = select(Session).where(Session.session_hash == session_hash)
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
            self._close_db_if_local(db)

    def get_current_user(self, session_id: str) -> Optional[UserResponse]:
        """Get the authenticated user for a given session ID."""
        if not session_id:
            return None
        db = self._get_db()
        try:
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()

            stmt = select(Session).where(
                Session.session_hash == session_hash,
                Session.revoked == False,
            )
            result = db.execute(stmt)
            session = result.scalar_one_or_none()

            if not session:
                return None

            # Check session expiry
            now = datetime.now(timezone.utc)
            session_expires = session.expires_at
            if session_expires.tzinfo is None:
                session_expires = session_expires.replace(tzinfo=timezone.utc)
            if session_expires < now:
                return None

            # Get the associated user
            stmt = select(User).where(User.id == session.user_id)
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
            self._close_db_if_local(db)
