from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class SupplierProjection(Base):
    __tablename__ = "supplier_projection"

    __table_args__ = (
        UniqueConstraint(
            "merchant_id",
            "supplier_code",
            name="uq_supplier_projection_merchant_supplier_code"
        ),
        UniqueConstraint(
            "merchant_id",
            "phone",
            name="uq_supplier_projection_merchant_phone"
        ),
        UniqueConstraint(
            "merchant_id",
            "email",
            name="uq_supplier_projection_merchant_email"
        ),
    )

    supplier_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    supplier_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    contact_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    tax_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    payment_terms: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True
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