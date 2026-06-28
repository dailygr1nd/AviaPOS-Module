from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    DateTime,
    BigInteger
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class PaymentProjection(Base):

    __tablename__ = (
        "payment_projection"
    )

    payment_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    amount: Mapped[float] = mapped_column(
        Float
    )

    payment_method: Mapped[str] = mapped_column(
        String(50)
    )

    reference_type: Mapped[str] = mapped_column(
        String(50)
    )

    reference_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    version: Mapped[int] = mapped_column(
        BigInteger,
        default=1
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )