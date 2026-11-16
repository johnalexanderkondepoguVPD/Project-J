from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from . import Base


class Examination(Base):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    abbreviation = Column(String(100), unique=True, index=True, nullable=True)
    conducting_body = Column(String(500), nullable=False)
    exam_type = Column(String(100), nullable=True)  # e.g., "UPSC", "SSC", "State PSC"
    level = Column(String(100), nullable=True)  # e.g., "National", "State", "Local"
    subject = Column(String(500), nullable=True)
    frequency = Column(String(100), nullable=True)  # e.g., "Annual", "Biennial"
    eligibility_criteria = Column(Text, nullable=True)
    exam_pattern = Column(JSON, nullable=True)
    syllabus = Column(Text, nullable=True)
    official_website = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Examination {self.name}>"