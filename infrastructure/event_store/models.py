from datetime import datetime

from sqlalchemy import (
    String,
    JSON,
    BigInteger,
    DateTime,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import Base


class EventModel(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    version: Mapped[int] = mapped_column(
    BigInteger,
    index=True
    )

    event_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
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

    previous_hash: Mapped[str] = mapped_column(
        Text
    )

    current_hash: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )