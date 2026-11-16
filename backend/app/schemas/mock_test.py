from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MockTestCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=500, description="Mock test title")
    examination_id: int = Field(..., description="ID of the examination")
    description: Optional[str] = Field(None, description="Mock test description")
    total_questions: Optional[int] = Field(None, description="Total number of questions")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")
    difficulty_level: Optional[str] = Field(
        None, description="Difficulty level: easy, medium, hard"
    )


class MockTestResponse(BaseModel):
    id: int
    title: str
    examination_id: int
    description: Optional[str] = None
    total_questions: Optional[int] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None
    is_active: bool
    is_published: bool
    average_score: Optional[float] = None
    pass_percentage: Optional[float] = None
    total_attempts: int
    created_at: datetime

    class Config:
        from_attributes = True


class MockTestListItem(BaseModel):
    id: int
    title: str
    examination_id: int
    description: Optional[str] = None
    is_published: bool
    total_attempts: int

    class Config:
        from_attributes = True