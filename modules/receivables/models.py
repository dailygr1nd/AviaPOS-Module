from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    Float,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class ReceivableProjection(Base):

    __tablename__ = "receivable_projection"

    receivable_id: Mapped[str] = mapped_column(
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

    customer_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    sale_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    amount: Mapped[float] = mapped_column(
        Float
    )

    paid_amount: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    balance: Mapped[float] = mapped_column(
        Float
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