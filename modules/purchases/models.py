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


class PurchaseProjection(Base):
    __tablename__ = "purchase_projection"

    purchase_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    branch_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    supplier_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    supplier_invoice_ref: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="CREATED",
        index=True
    )

    total: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    lines: Mapped[list] = mapped_column(
        JSON,
        default=list
    )

    received_items: Mapped[list] = mapped_column(
        JSON,
        default=list
    )

    received_by_user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
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