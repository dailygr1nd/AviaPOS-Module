from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
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


class AuthUserModel(Base):

    __tablename__ = "auth_users"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "username",

            name="uq_auth_users_merchant_username"

        ),

    )

    id: Mapped[int] = mapped_column(

        BigInteger,

        primary_key=True,

        autoincrement=True

    )

    user_id: Mapped[str] = mapped_column(

        String(100),

        unique=True,

        index=True

    )

    merchant_id: Mapped[str] = mapped_column(

        String(100),

        index=True

    )

    branch_id: Mapped[str | None] = mapped_column(

        String(100),

        nullable=True,

        index=True

    )

    username: Mapped[str] = mapped_column(

        String(100),

        index=True

    )

    password_hash: Mapped[str] = mapped_column(

        String(255)

    )

    role: Mapped[str] = mapped_column(

        String(50),

        index=True

    )

    active: Mapped[bool] = mapped_column(

        Boolean,

        default=True,

        index=True

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