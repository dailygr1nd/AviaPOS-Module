from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    JSON,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class IdempotencyRecordModel(Base):

    __tablename__ = "idempotency_records"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "idempotency_key",

            name="uq_idempotency_merchant_key"

        ),

    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(150),
        index=True
    )

    command_name: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    request_hash: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        index=True
    )

    response_payload: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )