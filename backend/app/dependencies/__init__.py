from typing import Optional
from fastapi import Cookie, HTTPException, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationException


http_bearer = HTTPBearer(auto_error=False)


async def get_db() -> AsyncSession:
    """Dependency to get a database session."""
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
) -> Optional["UserResponse"]:
    """Dependency to get the current authenticated user from session cookie.

    The session ID is sent as an opaque string through a secure HTTP cookie.
    The backend hashes it and looks up the corresponding active session.
    """
    from app.services.auth import AuthService

    if not session_id:
        return None

    auth_service = AuthService()
    user = auth_service.get_current_user(session_id)
    return user


async def get_optional_current_user(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
) -> Optional["UserResponse"]:
    """Dependency to get the current user optionally (for public endpoints)."""
    if not session_id:
        return None
    from app.services.auth import AuthService
    auth_service = AuthService()
    return auth_service.get_current_user(session_id)