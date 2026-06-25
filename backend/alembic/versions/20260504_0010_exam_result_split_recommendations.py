"""add split exam recommendations

Revision ID: 20260504_0010
Revises: 20260430_0009
Create Date: 2026-05-04 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260504_0010"
down_revision = "20260430_0009"
branch_labels = None
depends_on = None


def _json_type():
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        from sqlalchemy.dialects import postgresql

        return postgresql.JSONB()
    return sa.JSON()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("exam_results")}
    json_type = _json_type()
    can_alter_nullability = bind.dialect.name != "sqlite"

    if "positive_recommendations" not in columns:
        op.add_column("exam_results", sa.Column("positive_recommendations", json_type, nullable=True))
        op.execute("UPDATE exam_results SET positive_recommendations = '[]'")
        if can_alter_nullability:
            op.alter_column("exam_results", "positive_recommendations", nullable=False)

    if "improvement_recommendations" not in columns:
        op.add_column("exam_results", sa.Column("improvement_recommendations", json_type, nullable=True))
        op.execute("UPDATE exam_results SET improvement_recommendations = recommendations")
        if can_alter_nullability:
            op.alter_column("exam_results", "improvement_recommendations", nullable=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("exam_results")}

    if "improvement_recommendations" in columns:
        op.drop_column("exam_results", "improvement_recommendations")
    if "positive_recommendations" in columns:
        op.drop_column("exam_results", "positive_recommendations")
