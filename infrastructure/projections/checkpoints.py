from datetime import datetime

from sqlalchemy import (
    String,
    BigInteger,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import Base


class ProjectionCheckpoint(Base):

    __tablename__ = "projection_checkpoints"

    projection_name: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    last_event_id: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )