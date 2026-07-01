from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    JSON,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class PaymentCaptureProjection(Base):
    __tablename__ = "payment_capture_projection"

    __table_args__ = (
        UniqueConstraint(
            "merchant_id",
            "provider",
            "provider_reference",
            name="uq_payment_capture_merchant_provider_reference"
        ),
    )

    capture_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    branch_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    provider_channel: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    provider_reference: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    external_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    payer_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    payer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    amount: Mapped[float] = mapped_column(
        Float
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        index=True
    )

    payment_method: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    reference_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    payment_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    railone_intent_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    reconciliation_state: Mapped[str] = mapped_column(
        String(100),
        default="PENDING",
        index=True
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    raw_payload: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )

    capture_metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )

    version: Mapped[int] = mapped_column(
        BigInteger,
        default=1
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
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