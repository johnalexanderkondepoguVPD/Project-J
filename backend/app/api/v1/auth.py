from typing import Optional
from fastapi import APIRouter, Depends, Response, Request, status, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.dependencies import get_current_user
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
) -> UserResponse:
    """Register a new user and create an initial session."""
    auth_service = AuthService()
    return auth_service.register(user_data)


@router.post("/login", response_model=UserResponse)
def login(
    login_data: UserLogin,
    response: Response,
) -> UserResponse:
    """Authenticate user and create session cookie."""
    auth_service = AuthService()
    result = auth_service.login(login_data)
    user = result["user"]
    session_id = result["session_id"]

    # Set secure HTTP-only cookie with the session ID
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=30 * 24 * 60 * 60,
    )

    return user


@router.post("/logout")
def logout(
    response: Response,
    request: Request,
) -> dict:
    """Logout and revoke session cookie."""
    # Get session ID from cookie
    session_id = request.cookies.get("session_id", "")

    # Revoke the session
    auth_service = AuthService()
    auth_service.logout(session_id)

    # Clear the cookie
    response.delete_cookie(
        key="session_id",
        path="/",
        secure=True,
        samesite="lax",
    )

    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def me(
    current_user: Optional[UserResponse] = Depends(get_current_user),
) -> UserResponse:
    """Get the current authenticated user."""
    if not current_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return current_user