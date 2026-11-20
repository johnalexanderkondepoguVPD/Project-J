from typing import Optional, Generator
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserResponse
from app.services.auth import AuthService
from app.database import SessionLocal


http_bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get a synchronous database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def extract_session_id(
    request: Request,
    bearer_creds: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> Optional[str]:
    """Extract session ID from cookie or Authorization Bearer header."""
    # 1. Check configured cookie name
    session_id = request.cookies.get(settings.session_cookie_name)
    if session_id:
        return session_id

    # 2. Check fallback cookie name 'session_id'
    session_id = request.cookies.get("session_id")
    if session_id:
        return session_id

    # 3. Check Authorization header
    if bearer_creds and bearer_creds.credentials:
        return bearer_creds.credentials

    return None


async def get_current_user(
    request: Request,
    bearer_creds: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> Optional[UserResponse]:
    """Dependency to get the current user, or None if unauthenticated."""
    session_id = extract_session_id(request, bearer_creds)
    if not session_id:
        return None

    auth_service = AuthService()
    return auth_service.get_current_user(session_id)


async def get_current_active_user(
    current_user: Optional[UserResponse] = Depends(get_current_user),
) -> UserResponse:
    """Dependency to enforce that user is authenticated and active."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
