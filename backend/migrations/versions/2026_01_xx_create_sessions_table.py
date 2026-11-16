"""create sessions table

Revision ID: 2026_01_xx_create_sessions_table
Revises: 
Create Date: 2026-01-XX 00:00:00.000000

"""
import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    UUID,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func

from app.database import Base
from alembic import op


# revision identifiers, used by Alembic.
revision = "2026_01_xx_create_sessions_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sessions",
        Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column("session_hash", String(64), unique=True, nullable=False),
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
        Column("expires_at", DateTime(timezone=True), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Column("revoked", Boolean, default=False),
    )
    op.add_index("ix_sessions_session_hash", "sessions", ["session_hash"], unique=True)
    op.add_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.add_index("ix_sessions_expires_at", "sessions", ["expires_at"])


def downgrade():
    op.drop_table("sessions")