from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import Subject, enum_values


class DiagnosticProfile(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "diagnostic_profiles"
    __table_args__ = (
        UniqueConstraint("user_id", "subject", name="uq_diagnostic_profiles_user_subject"),
    )

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject: Mapped[Subject] = mapped_column(
        Enum(Subject, name="subject", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    topic_results: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    bloom_results: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    strengths: Mapped[list[str]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    weaknesses: Mapped[list[str]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    positive_recommendations: Mapped[list[str]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    improvement_recommendations: Mapped[list[str]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)

    user = relationship("User", back_populates="diagnostic_profiles")
