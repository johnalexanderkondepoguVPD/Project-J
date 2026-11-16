from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from . import Base


class MockTest(Base):
    __tablename__ = "mock_tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    examination_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    
    # Test configuration
    total_questions = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    difficulty_level = Column(String(50), nullable=True)
    
    # Test state
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # Results
    average_score = Column(Float, nullable=True)
    pass_percentage = Column(Float, nullable=True)
    total_attempts = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<MockTest {self.title}>"