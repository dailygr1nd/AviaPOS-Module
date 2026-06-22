from sqlalchemy import (
    String,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class InventoryProjection(Base):

    __tablename__ = (
        "inventory_projection"
    )

    branch_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )