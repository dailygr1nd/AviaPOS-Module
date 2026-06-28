from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    JSON,
    Text,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class OutboxMessageModel(Base):

    __tablename__ = "outbox_messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    message_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )

    event_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    aggregate_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        index=True
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )