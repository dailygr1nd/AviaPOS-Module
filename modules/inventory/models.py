from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    Integer,
    PrimaryKeyConstraint,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class InventoryProjection(Base):

    __tablename__ = "inventory_projection"

    __table_args__ = (

        PrimaryKeyConstraint(

            "merchant_id",

            "branch_id",

            "product_id",

            name="pk_inventory_projection"

        ),

    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    branch_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    last_cost_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    version: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )