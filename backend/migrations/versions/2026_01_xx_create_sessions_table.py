"""create users and sessions tables

Revision ID: 2026_01_xx_create_sessions_table
Revises: 
Create Date: 2026-01-01 00:00:00.000000

"""
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Uuid,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func
from alembic import op


# revision identifiers, used by Alembic.
revision = "2026_01_xx_create_sessions_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create users table
    op.create_table(
        "users",
        Column("id", Uuid, primary_key=True, default=uuid.uuid4),
        Column("email", String(255), unique=True, nullable=False),
        Column("username", String(100), unique=True, nullable=False),
        Column("hashed_password", String(255), nullable=False),
        Column("full_name", String(255), nullable=True),
        Column("is_active", Boolean, default=True, nullable=False),
        Column("is_superuser", Boolean, default=False, nullable=False),
        Column("is_verified", Boolean, default=False, nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("updated_at", DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # 2. Create sessions table
    op.create_table(
        "sessions",
        Column("id", Uuid, primary_key=True, default=uuid.uuid4),
        Column("session_hash", String(64), unique=True, nullable=False),
        Column("user_id", Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        Column("expires_at", DateTime(timezone=True), nullable=False),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("revoked", Boolean, default=False, nullable=False),
    )
    op.create_index("ix_sessions_session_hash", "sessions", ["session_hash"], unique=True)
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_expires_at", "sessions", ["expires_at"])


def downgrade():
    op.drop_table("sessions")
    op.drop_table("users")
