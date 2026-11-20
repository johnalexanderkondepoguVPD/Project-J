from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExaminationCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Civil Services Examination",
                "abbreviation": "UPSC CSE",
                "conducting_body": "Union Public Service Commission",
                "exam_type": "UPSC",
                "level": "National",
                "subject": "General Studies & Optional",
                "frequency": "Annual",
                "eligibility_criteria": "Bachelor's degree from a recognized university. Age 21-32.",
                "exam_pattern": {
                    "stages": ["Preliminary", "Mains", "Personality Test"],
                    "total_marks": 2025,
                },
                "syllabus": "History, Geography, Polity, Economy, Environment, Current Affairs.",
                "official_website": "https://upsc.gov.in",
            }
        }
    )

    name: str = Field(..., min_length=3, max_length=500, description="Full examination name")
    abbreviation: Optional[str] = Field(None, max_length=100, description="Abbreviated name or acronym")
    conducting_body: str = Field(..., min_length=2, max_length=500, description="Organization conducting the exam")
    exam_type: str = Field(..., min_length=2, max_length=100, description="Exam category (e.g., UPSC, SSC, Banking, Railways)")
    level: str = Field("National", min_length=2, max_length=100, description="Jurisdiction level: National, State, Local")
    subject: Optional[str] = Field(None, max_length=500, description="Subject domain")
    frequency: Optional[str] = Field("Annual", description="Frequency: Annual, Biennial, Multiple Shifts")
    eligibility_criteria: Optional[str] = Field(None, description="Detailed eligibility criteria")
    exam_pattern: Optional[Dict[str, Any]] = Field(None, description="Configurable stages, marks, and negative marking")
    syllabus: Optional[str] = Field(None, description="Syllabus overview")
    official_website: Optional[str] = Field(None, max_length=500, description="Official portal URL")


class ExaminationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=500)
    abbreviation: Optional[str] = Field(None, max_length=100)
    conducting_body: Optional[str] = Field(None, min_length=2)
    exam_type: Optional[str] = Field(None, min_length=2)
    level: Optional[str] = Field(None, min_length=2)
    subject: Optional[str] = Field(None, max_length=500)
    frequency: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    exam_pattern: Optional[Dict[str, Any]] = None
    syllabus: Optional[str] = None
    official_website: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class ExaminationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    abbreviation: Optional[str] = None
    conducting_body: str
    exam_type: str
    level: str
    subject: Optional[str] = None
    frequency: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    exam_pattern: Optional[Dict[str, Any]] = None
    syllabus: Optional[str] = None
    official_website: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginatedExaminationResponse(BaseModel):
    items: List[ExaminationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ExamBodySummary(BaseModel):
    conducting_body: str
    exam_type: str
    exam_count: int
