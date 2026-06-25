"""initial schema

Revision ID: 20260320_0001
Revises:
Create Date: 2026-03-20 12:10:00.000000
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql


revision = "20260320_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    user_level = postgresql.ENUM(
        "basic",
        "intermediate",
        "advanced",
        name="user_level",
        create_type=True,
    )
    experiment_group = postgresql.ENUM(
        "control",
        "treatment",
        name="experiment_group",
        create_type=True,
    )
    user_role = postgresql.ENUM(
        "student",
        "admin",
        name="user_role",
        create_type=True,
    )
    session_status = postgresql.ENUM(
        "active",
        "revoked",
        "expired",
        name="session_status",
        create_type=True,
    )
    conversation_status = postgresql.ENUM(
        "active",
        "completed",
        "abandoned",
        name="conversation_status",
        create_type=True,
    )
    message_role = postgresql.ENUM(
        "system",
        "user",
        "assistant",
        name="message_role",
        create_type=True,
    )

    bind = op.get_bind()
    user_level.create(bind, checkfirst=True)
    experiment_group.create(bind, checkfirst=True)
    user_role.create(bind, checkfirst=True)
    session_status.create(bind, checkfirst=True)
    conversation_status.create(bind, checkfirst=True)
    message_role.create(bind, checkfirst=True)

    user_level_ref = postgresql.ENUM(
        "basic",
        "intermediate",
        "advanced",
        name="user_level",
        create_type=False,
    )
    experiment_group_ref = postgresql.ENUM(
        "control",
        "treatment",
        name="experiment_group",
        create_type=False,
    )
    user_role_ref = postgresql.ENUM(
        "student",
        "admin",
        name="user_role",
        create_type=False,
    )
    session_status_ref = postgresql.ENUM(
        "active",
        "revoked",
        "expired",
        name="session_status",
        create_type=False,
    )
    conversation_status_ref = postgresql.ENUM(
        "active",
        "completed",
        "abandoned",
        name="conversation_status",
        create_type=False,
    )
    message_role_ref = postgresql.ENUM(
        "system",
        "user",
        "assistant",
        name="message_role",
        create_type=False,
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("level", user_level_ref, nullable=False),
        sa.Column("experiment_group", experiment_group_ref, nullable=False),
        sa.Column("role", user_role_ref, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("status", session_status_ref, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("refresh_token_hash", name="uq_auth_sessions_refresh_token_hash"),
    )

    op.create_table(
        "conversations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("status", conversation_status_ref, nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("conversation_id", sa.String(length=36), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", message_role_ref, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("model_used", sa.String(length=100), nullable=True),
        sa.Column("rag_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_conversation_messages_conversation_id", "conversation_messages", ["conversation_id"], unique=False)

    # event_logs removed

    op.create_table(
        "documents",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("source", sa.String(length=500), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("level", user_level_ref, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(768), nullable=True),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_documents_source", "documents", ["source"], unique=False)
    op.create_index("ix_documents_topic", "documents", ["topic"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_documents_topic", table_name="documents")
    op.drop_index("ix_documents_source", table_name="documents")
    op.drop_table("documents")
    # event_logs removed
    op.drop_index("ix_conversation_messages_conversation_id", table_name="conversation_messages")
    op.drop_table("conversation_messages")
    op.drop_table("conversations")
    op.drop_table("auth_sessions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    sa.Enum(name="message_role").drop(bind, checkfirst=True)
    sa.Enum(name="conversation_status").drop(bind, checkfirst=True)
    sa.Enum(name="session_status").drop(bind, checkfirst=True)
    sa.Enum(name="user_role").drop(bind, checkfirst=True)
    sa.Enum(name="experiment_group").drop(bind, checkfirst=True)
    sa.Enum(name="user_level").drop(bind, checkfirst=True)
