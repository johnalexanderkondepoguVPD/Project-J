from typing import Optional
from fastapi import APIRouter, Depends, Response, Request, status, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import settings
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.dependencies import get_current_user, get_current_active_user, extract_session_id
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


def _set_session_cookie(response: Response, session_id: str) -> None:
    """Set the session cookie with application-configured security attributes."""
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        path="/",
        max_age=settings.session_expire_days * 24 * 60 * 60,
    )


def _clear_session_cookie(response: Response) -> None:
    """Clear session cookie(s) from the client."""
    response.delete_cookie(
        key=settings.session_cookie_name,
        path="/",
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
    )
    if settings.session_cookie_name != "session_id":
        response.delete_cookie(
            key="session_id",
            path="/",
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite,
        )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Registers a new student account, securely hashes the password using Argon2id, "
        "creates an active session in the database, and sets an HTTP-only session cookie "
        "so the user is signed in immediately."
    ),
    responses={
        201: {"description": "User created and authenticated successfully"},
        422: {"description": "Validation error or duplicate email/username"},
    },
)
def register(
    user_data: UserCreate,
    response: Response,
) -> UserResponse:
    """Register a new user and set the session cookie for automatic sign-in."""
    auth_service = AuthService()
    result = auth_service.register(user_data)
    _set_session_cookie(response, result["session_id"])
    return result["user"]


@router.post(
    "/login",
    response_model=UserResponse,
    summary="User sign in",
    description=(
        "Authenticates a user via email or username and password. "
        "Upon successful verification, generates an opaque cryptographically secure session ID, "
        "persists its SHA-256 hash in the database, and returns the session cookie."
    ),
    responses={
        200: {"description": "Successfully authenticated"},
        401: {"description": "Invalid credentials or disabled account"},
    },
)
def login(
    login_data: UserLogin,
    response: Response,
) -> UserResponse:
    """Authenticate user and create session cookie."""
    auth_service = AuthService()
    result = auth_service.login(login_data)
    _set_session_cookie(response, result["session_id"])
    return result["user"]


@router.post(
    "/logout",
    summary="User sign out",
    description="Revokes the active session in the database and clears the session cookie from the client.",
    responses={
        200: {"description": "Logged out successfully"},
    },
)
def logout(
    response: Response,
    request: Request,
) -> dict:
    """Logout and revoke session cookie."""
    session_id = extract_session_id(request)
    if session_id:
        auth_service = AuthService()
        auth_service.logout(session_id)

    _clear_session_cookie(response)
    return {"detail": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description=(
        "Fetches the user profile for the currently authenticated request. "
        "Accepts either an HTTP session cookie (`project_j_session`) or an `Authorization: Bearer <token>` header."
    ),
    responses={
        200: {"description": "Current user profile"},
        401: {"description": "Not authenticated or session expired/revoked"},
    },
)
def me(
    current_user: UserResponse = Depends(get_current_active_user),
) -> UserResponse:
    """Get the current authenticated user."""
    return current_user
