"""subject based academic modules

Revision ID: 20260405_0002
Revises: 20260320_0001
Create Date: 2026-04-05 19:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260405_0002"
down_revision = "20260320_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    subject = postgresql.ENUM(
        "precalculo",
        "preuniversitario",
        name="subject",
        create_type=True,
    )
    attempt_status = postgresql.ENUM(
        "in_progress",
        "completed",
        "abandoned",
        name="attempt_status",
        create_type=True,
    )
    question_type = postgresql.ENUM(
        "multiple_choice",
        name="question_type",
        create_type=True,
    )

    subject.create(bind, checkfirst=True)
    attempt_status.create(bind, checkfirst=True)
    question_type.create(bind, checkfirst=True)

    subject_ref = postgresql.ENUM(
        "precalculo",
        "preuniversitario",
        name="subject",
        create_type=False,
    )
    attempt_status_ref = postgresql.ENUM(
        "in_progress",
        "completed",
        "abandoned",
        name="attempt_status",
        create_type=False,
    )
    question_type_ref = postgresql.ENUM(
        "multiple_choice",
        name="question_type",
        create_type=False,
    )

    op.add_column("users", sa.Column("subject", subject_ref, nullable=True))
    op.execute("UPDATE users SET subject = 'precalculo'")
    op.alter_column("users", "subject", nullable=False)
    op.drop_column("users", "experiment_group")
    op.drop_column("users", "level")

    op.add_column("documents", sa.Column("subject", subject_ref, nullable=True))
    op.execute("UPDATE documents SET subject = 'precalculo'")
    op.alter_column("documents", "subject", nullable=False)
    op.drop_column("documents", "level")

    op.create_table(
        "diagnostic_questions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("skill", sa.String(length=200), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("question_type", question_type_ref, nullable=False),
        sa.Column("options_json", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.String(length=255), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_diagnostic_questions_subject", "diagnostic_questions", ["subject"], unique=False)
    op.create_index("ix_diagnostic_questions_topic", "diagnostic_questions", ["topic"], unique=False)

    op.create_table(
        "diagnostic_attempts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("status", attempt_status_ref, nullable=False),
        sa.Column("score_global", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_diagnostic_attempts_user_id", "diagnostic_attempts", ["user_id"], unique=False)
    op.create_index("ix_diagnostic_attempts_subject", "diagnostic_attempts", ["subject"], unique=False)

    op.create_table(
        "diagnostic_responses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("attempt_id", sa.String(length=36), sa.ForeignKey("diagnostic_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", sa.String(length=36), sa.ForeignKey("diagnostic_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("answer_text", sa.String(length=255), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("score_item", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("attempt_id", "question_id", name="uq_diagnostic_responses_attempt_question"),
    )
    op.create_index("ix_diagnostic_responses_attempt_id", "diagnostic_responses", ["attempt_id"], unique=False)
    op.create_index("ix_diagnostic_responses_question_id", "diagnostic_responses", ["question_id"], unique=False)

    op.create_table(
        "diagnostic_profiles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("topic_results", sa.JSON(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("weaknesses", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "subject", name="uq_diagnostic_profiles_user_subject"),
    )
    op.create_index("ix_diagnostic_profiles_user_id", "diagnostic_profiles", ["user_id"], unique=False)
    op.create_index("ix_diagnostic_profiles_subject", "diagnostic_profiles", ["subject"], unique=False)

    op.create_table(
        "exam_templates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_integrator", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_exam_templates_subject", "exam_templates", ["subject"], unique=False)
    op.create_index("ix_exam_templates_topic", "exam_templates", ["topic"], unique=False)

    op.create_table(
        "exam_questions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("exam_template_id", sa.String(length=36), sa.ForeignKey("exam_templates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("skill", sa.String(length=200), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("question_type", question_type_ref, nullable=False),
        sa.Column("options_json", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.String(length=255), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_exam_questions_exam_template_id", "exam_questions", ["exam_template_id"], unique=False)
    op.create_index("ix_exam_questions_topic", "exam_questions", ["topic"], unique=False)

    op.create_table(
        "exam_attempts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exam_template_id", sa.String(length=36), sa.ForeignKey("exam_templates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("status", attempt_status_ref, nullable=False),
        sa.Column("score_global", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_exam_attempts_user_id", "exam_attempts", ["user_id"], unique=False)
    op.create_index("ix_exam_attempts_exam_template_id", "exam_attempts", ["exam_template_id"], unique=False)
    op.create_index("ix_exam_attempts_subject", "exam_attempts", ["subject"], unique=False)

    op.create_table(
        "exam_responses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("attempt_id", sa.String(length=36), sa.ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", sa.String(length=36), sa.ForeignKey("exam_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("answer_text", sa.String(length=255), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("score_item", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("attempt_id", "question_id", name="uq_exam_responses_attempt_question"),
    )
    op.create_index("ix_exam_responses_attempt_id", "exam_responses", ["attempt_id"], unique=False)
    op.create_index("ix_exam_responses_question_id", "exam_responses", ["question_id"], unique=False)

    op.create_table(
        "exam_results",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("exam_attempt_id", sa.String(length=36), sa.ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score_global", sa.Float(), nullable=False),
        sa.Column("topic_breakdown", sa.JSON(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("weaknesses", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("exam_attempt_id", name="uq_exam_results_attempt"),
    )
    op.create_index("ix_exam_results_exam_attempt_id", "exam_results", ["exam_attempt_id"], unique=False)

    sa.Enum(name="experiment_group").drop(bind, checkfirst=True)
    sa.Enum(name="user_level").drop(bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()

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
    user_level.create(bind, checkfirst=True)
    experiment_group.create(bind, checkfirst=True)

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

    op.drop_index("ix_exam_results_exam_attempt_id", table_name="exam_results")
    op.drop_table("exam_results")
    op.drop_index("ix_exam_responses_question_id", table_name="exam_responses")
    op.drop_index("ix_exam_responses_attempt_id", table_name="exam_responses")
    op.drop_table("exam_responses")
    op.drop_index("ix_exam_attempts_subject", table_name="exam_attempts")
    op.drop_index("ix_exam_attempts_exam_template_id", table_name="exam_attempts")
    op.drop_index("ix_exam_attempts_user_id", table_name="exam_attempts")
    op.drop_table("exam_attempts")
    op.drop_index("ix_exam_questions_topic", table_name="exam_questions")
    op.drop_index("ix_exam_questions_exam_template_id", table_name="exam_questions")
    op.drop_table("exam_questions")
    op.drop_index("ix_exam_templates_topic", table_name="exam_templates")
    op.drop_index("ix_exam_templates_subject", table_name="exam_templates")
    op.drop_table("exam_templates")
    op.drop_index("ix_diagnostic_profiles_subject", table_name="diagnostic_profiles")
    op.drop_index("ix_diagnostic_profiles_user_id", table_name="diagnostic_profiles")
    op.drop_table("diagnostic_profiles")
    op.drop_index("ix_diagnostic_responses_question_id", table_name="diagnostic_responses")
    op.drop_index("ix_diagnostic_responses_attempt_id", table_name="diagnostic_responses")
    op.drop_table("diagnostic_responses")
    op.drop_index("ix_diagnostic_attempts_subject", table_name="diagnostic_attempts")
    op.drop_index("ix_diagnostic_attempts_user_id", table_name="diagnostic_attempts")
    op.drop_table("diagnostic_attempts")
    op.drop_index("ix_diagnostic_questions_topic", table_name="diagnostic_questions")
    op.drop_index("ix_diagnostic_questions_subject", table_name="diagnostic_questions")
    op.drop_table("diagnostic_questions")

    op.add_column("documents", sa.Column("level", user_level_ref, nullable=True))
    op.execute("UPDATE documents SET level = 'basic'")
    op.alter_column("documents", "level", nullable=False)
    op.drop_column("documents", "subject")

    op.add_column("users", sa.Column("level", user_level_ref, nullable=True))
    op.add_column("users", sa.Column("experiment_group", experiment_group_ref, nullable=True))
    op.execute("UPDATE users SET level = 'basic', experiment_group = 'treatment'")
    op.alter_column("users", "level", nullable=False)
    op.alter_column("users", "experiment_group", nullable=False)
    op.drop_column("users", "subject")

    sa.Enum(name="question_type").drop(bind, checkfirst=True)
    sa.Enum(name="attempt_status").drop(bind, checkfirst=True)
    sa.Enum(name="subject").drop(bind, checkfirst=True)
