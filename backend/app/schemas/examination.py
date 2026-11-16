from pydantic import BaseModel, Field, StringConstraints
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExaminationCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=500, description="Full examination name")
    abbreviation: Optional[str] = Field(None, max_length=100, description="Abbreviated name/acronym")
    conducting_body: str = Field(..., min_length=3, description="Organization conducting the exam")
    exam_type: str = Field(..., min_length=3, description="Type: UPSC, SSC, State PSC, etc.")
    level: str = Field(..., min_length=3, description="Level: National, State, Local")
    subject: Optional[str] = Field(None, max_length=500, description="Subject area")
    frequency: Optional[str] = Field(None, description="Frequency: Annual, Biennial, etc.")
    eligibility_criteria: Optional[str] = Field(None, description="Eligibility criteria")
    exam_pattern: Optional[Dict[str, Any]] = Field(None, description="Exam pattern JSON")
    syllabus: Optional[str] = Field(None, description="Syllabus content")
    official_website: Optional[str] = Field(None, max_length=500, description="Official website URL")


class ExaminationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=500)
    abbreviation: Optional[str] = Field(None, max_length=100)
    conducting_body: Optional[str] = Field(None, min_length=3)
    exam_type: Optional[str] = Field(None, min_length=3)
    level: Optional[str] = Field(None, min_length=3)
    subject: Optional[str] = Field(None, max_length=500)
    frequency: Optional[str] = Field(None)
    eligibility_criteria: Optional[str] = Field(None)
    exam_pattern: Optional[Dict[str, Any]] = Field(None)
    syllabus: Optional[str] = Field(None)
    official_website: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = Field(None)


class ExaminationResponse(BaseModel):
    id: int
    name: str
    abbreviation: Optional[str] = None
    conducting_body: str
    exam_type: str
    level: str
    subject: Optional[str] = None
    frequency: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExaminationListItem(BaseModel):
    id: int
    name: str
    conducting_body: str
    exam_type: str
    level: str
    is_active: bool

    class Config:
        from_attributes = True