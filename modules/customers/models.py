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


class CustomerProjection(Base):

    __tablename__ = "customer_projection"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "phone",

            name="uq_customer_projection_merchant_phone"

        ),

        UniqueConstraint(

            "merchant_id",

            "email",

            name="uq_customer_projection_merchant_email"

        ),

    )

    customer_id: Mapped[str] = mapped_column(

        String(100),

        primary_key=True

    )

    merchant_id: Mapped[str] = mapped_column(

        String(100),

        index=True

    )

    name: Mapped[str] = mapped_column(

        String(255),

        index=True

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

    customer_type: Mapped[str] = mapped_column(

        String(50),

        default="REGULAR",

        index=True

    )

    tax_id: Mapped[str | None] = mapped_column(

        String(100),

        nullable=True,

        index=True

    )

    credit_limit: Mapped[float] = mapped_column(

        Float,

        default=0

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