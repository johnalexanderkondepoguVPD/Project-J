import uuid
import hashlib
from datetime import datetime, timedelta

from sqlalchemy import Column, String, DateTime, Boolean, UUID, Text, Index, ForeignKey
from sqlalchemy.sql import func
from . import Base


def _hash_session_id(session_id: str) -> str:
    """SHA-256 hash of session ID for database storage."""
    return hashlib.sha256(session_id.encode()).hexdigest()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_hash = Column(String(64), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked = Column(Boolean, default=False)

    __table_args__ = (
        Index("ix_sessions_session_hash", "session_hash", unique=True),
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_expires_at", "expires_at"),
    )

    def __repr__(self):
        return f"<Session {self.session_hash[:8]}... for user {self.user_id}>"

    @staticmethod
    def create_session_hash(session_id: str) -> str:
        return _hash_session_id(session_id)

    @staticmethod
    def verify_session_hash(session_hash: str) -> bool:
        """Validate that session_hash is a valid SHA-256 hex digest."""
        return len(session_hash) == 64 and all(
            c in "0123456789abcdef" for c in session_hash
        )