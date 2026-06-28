from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    JSON,
    String
)

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class TransferProjection(Base):
    __tablename__ = "transfer_projection"

    transfer_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    transfer_type: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    source_branch_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    destination_branch_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    destination_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    destination_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    amount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    currency: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True,
        index=True
    )

    purpose: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    rail_hint: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    external_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    provider_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    railone_intent_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    reconciliation_state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    items: Mapped[list] = mapped_column(
        JSON,
        default=list
    )

    dispatched_items: Mapped[list] = mapped_column(
        JSON,
        default=list
    )

    received_items: Mapped[list] = mapped_column(
        JSON,
        default=list
    )

    dispatched_by_user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    received_by_user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    transfer_metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )

    version: Mapped[int] = mapped_column(
        BigInteger,
        default=1
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )