from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    JSON,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class SaleProjection(Base):

    __tablename__ = "sale_projection"

    sale_id: Mapped[str] = mapped_column(
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

    customer_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    total: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    lines: Mapped[list] = mapped_column(
        JSON,
        default=list
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