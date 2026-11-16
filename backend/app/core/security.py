# JWT Authentication for Project-J

import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from .config import settings

def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    secret_key: str | None = None,
    algorithm: str = "HS256",
) -> str:
    """Create a JWT access token."""
    if secret_key is None:
        secret_key = settings.secret_key
    
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(
    token: str,
    secret_key: str | None = None,
    algorithm: str = "HS256",
) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    if secret_key is None:
        secret_key = settings.secret_key
    
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    return payload


def verify_token(token: str, secret_key: str | None = None) -> Optional[str]:
    """Verify JWT token and return the subject (user ID/username)."""
    try:
        payload = decode_access_token(token, secret_key)
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return subject
    except Exception:
        return None