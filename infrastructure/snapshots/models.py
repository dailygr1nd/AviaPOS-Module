from datetime import datetime

from sqlalchemy import (
    String,
    JSON,
    DateTime,
    BigInteger
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import Base


class SnapshotModel(Base):

    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    aggregate_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    aggregate_type: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    version: Mapped[int] = mapped_column(
        BigInteger
    )

    state: Mapped[dict] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )