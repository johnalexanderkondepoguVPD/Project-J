import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "aspirant@example.com",
                "username": "aspirant2026",
                "full_name": "Aspirant Kumar",
                "password": "SecurePassword123!",
            }
        }
    )

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name of user")
    password: str = Field(..., min_length=8, description="Password (at least 8 characters)")


class UserLogin(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "identifier": "aspirant@example.com",
                "password": "SecurePassword123!",
            }
        }
    )

    identifier: str = Field(..., description="Username or email address")
    password: str = Field(..., description="Account password")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None