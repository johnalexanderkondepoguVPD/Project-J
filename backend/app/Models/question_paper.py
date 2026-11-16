from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, UniqueConstraint
from sqlalchemy.sql import func
from . import Base


class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(Integer, primary_key=True, index=True)
    examination_id = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    year = Column(Integer, nullable=False)
    url = Column(String(500), nullable=False)
    file_path = Column(String(500), nullable=True)
    storage_type = Column(String(50), nullable=True)  # "s3", "local", "url"
    pdf_text = Column(Text, nullable=True)
    ocr_status = Column(String(50), nullable=True, default="pending")
    ocr_error = Column(Text, nullable=True)
    difficulty_analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("examination_id", "year", name="uq_examination_year"),
    )

    def __repr__(self):
        return f"<QuestionPaper {self.title} ({self.year})>"