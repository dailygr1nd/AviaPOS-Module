from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class ProductProjection(Base):

    __tablename__ = "product_projection"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "sku",

            name="uq_product_projection_merchant_sku"

        ),

    )

    product_id: Mapped[str] = mapped_column(

        String(100),

        primary_key=True

    )

    merchant_id: Mapped[str] = mapped_column(

        String(100),

        index=True

    )

    sku: Mapped[str] = mapped_column(

        String(100),

        index=True

    )

    name: Mapped[str] = mapped_column(

        String(255),

        index=True

    )

    selling_price: Mapped[float] = mapped_column(

        Float

    )

    cost_price: Mapped[float] = mapped_column(

        Float

    )

    category: Mapped[str | None] = mapped_column(

        String(100),

        nullable=True,

        index=True

    )

    barcode: Mapped[str | None] = mapped_column(

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