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


class BranchProjection(Base):
    __tablename__ = "branch_projection"

    __table_args__ = (
        UniqueConstraint(
            "merchant_id",
            "branch_code",
            name="uq_branch_projection_merchant_branch_code"
        ),
    )

    branch_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    branch_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    location: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    manager_user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
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