from app.core.database import Base
from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import MessageRole, enum_values


class ConversationMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "conversation_messages"

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole, name="message_role", values_callable=enum_values),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rag_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    conversation = relationship("Conversation", back_populates="messages")
