from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Index
from sqlalchemy.sql import func
from app.database import Base


class Examination(Base):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(500), nullable=False, index=True)
    abbreviation = Column(String(100), unique=True, index=True, nullable=True)
    conducting_body = Column(String(500), nullable=False, index=True)
    exam_type = Column(String(100), nullable=True, index=True)  # e.g., "UPSC", "SSC", "Banking", "Railways"
    level = Column(String(100), nullable=True, default="National")  # e.g., "National", "State", "Local"
    subject = Column(String(500), nullable=True)
    frequency = Column(String(100), nullable=True, default="Annual")
    eligibility_criteria = Column(Text, nullable=True)
    exam_pattern = Column(JSON, nullable=True)
    syllabus = Column(Text, nullable=True)
    official_website = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        Index("ix_examinations_body_type", "conducting_body", "exam_type"),
    )

    def __repr__(self):
        return f"<Examination {self.abbreviation or self.name}>"
