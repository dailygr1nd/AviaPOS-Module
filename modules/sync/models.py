from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    JSON,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from infrastructure.database.base import (
    Base
)


class SyncDeviceModel(Base):

    __tablename__ = "sync_devices"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "device_id",

            name="uq_sync_device_merchant_device"

        ),

    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
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

    user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    device_id: Mapped[str] = mapped_column(
        String(150),
        index=True
    )

    device_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        default="ANDROID"
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="ACTIVE",
        index=True
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


class SyncInboxEventModel(Base):

    __tablename__ = "sync_inbox_events"

    __table_args__ = (

        UniqueConstraint(

            "merchant_id",

            "device_id",

            "client_event_id",

            name="uq_sync_inbox_merchant_device_client_event"

        ),

    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
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

    device_id: Mapped[str] = mapped_column(
        String(150),
        index=True
    )

    client_event_id: Mapped[str] = mapped_column(
        String(150),
        index=True
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(200),
        index=True
    )

    command_name: Mapped[str] = mapped_column(
        String(120),
        index=True
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    expected_version: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="RECEIVED",
        index=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )