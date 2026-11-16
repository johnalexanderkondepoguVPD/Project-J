from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, UniqueConstraint
from sqlalchemy.sql import func
from . import Base


class PatternAnalysis(Base):
    __tablename__ = "pattern_analyses"

    id = Column(Integer, primary_key=True, index=True)
    question_paper_id = Column(Integer, nullable=False)
    examination_id = Column(Integer, nullable=False)
    
    # Pattern metrics
    year = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=True)
    subjects_covered = Column(JSON, nullable=True)
    topics_frequent = Column(JSON, nullable=True)
    topics_new = Column(JSON, nullable=True)
    difficulty_distribution = Column(JSON, nullable=True)
    subject_weightage = Column(JSON, nullable=True)
    
    # Temporal patterns
    year_trend = Column(String(50), nullable=True)  # "improving", "declining", "stable"
    gap_from_previous = Column(Integer, nullable=True)  # years gap
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("question_paper_id", name="uq_question_paper_id"),
    )

    def __repr__(self):
        return f"<PatternAnalysis for {self.examination_id} - {self.year}>"