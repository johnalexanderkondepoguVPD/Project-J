from pydantic import BaseModel, Field, StringConstraints
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuestionPaperUpload(BaseModel):
    examination_id: int = Field(..., description="ID of the examination")
    title: str = Field(..., min_length=3, max_length=500, description="Question paper title")
    year: int = Field(..., ge=1900, le=2030, description="Exam year")
    url: str = Field(..., description="Source URL or file path")
    storage_type: Optional[str] = Field(
        None, 
        description="Storage type: s3, local, url"
    )


class QuestionPaperResponse(BaseModel):
    id: int
    examination_id: int
    title: str
    year: int
    url: str
    storage_type: Optional[str] = None
    pdf_text: Optional[str] = None
    ocr_status: Optional[str] = None
    ocr_error: Optional[str] = None
    difficulty_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionPaperSearch(BaseModel):
    query: Optional[str] = Field(None, description="Search query for title/year")
    examination_id: Optional[int] = Field(None, description="Filter by examination")
    year: Optional[int] = Field(None, description="Filter by year")
    ocr_status: Optional[str] = Field(None, description="Filter by OCR status")