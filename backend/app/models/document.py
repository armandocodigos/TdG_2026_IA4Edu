from app.core.database import Base
from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, TypeDecorator

try:
    from pgvector.sqlalchemy import Vector
except ModuleNotFoundError:  # pragma: no cover - fallback for local environments without pgvector
    class Vector:  # type: ignore[override]
        def __init__(self, dimensions: int) -> None:
            self.dimensions = dimensions

from app.core.config import get_settings
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import Subject, enum_values


class EmbeddingType(TypeDecorator):
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(Vector(get_settings().embedding_dimensions))
        return dialect.type_descriptor(JSON())


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "documents"

    source: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    subject: Mapped[Subject] = mapped_column(
        Enum(Subject, name="subject", values_callable=enum_values),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(EmbeddingType(), nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )
