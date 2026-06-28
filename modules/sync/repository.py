from datetime import datetime

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from infrastructure.event_store.models import (
    EventModel
)

from modules.sync.models import (
    SyncDeviceModel,
    SyncInboxEventModel
)


class SyncRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def register_device(

        self,

        merchant_id: str,

        device_id: str,

        branch_id: str | None = None,

        user_id: str | None = None,

        device_name: str | None = None,

        platform: str = "ANDROID"

    ):

        existing = (

            self.db.query(
                SyncDeviceModel
            )

            .filter(
                SyncDeviceModel.merchant_id
                == merchant_id,

                SyncDeviceModel.device_id
                == device_id

            )

            .first()

        )

        if existing:

            existing.branch_id = branch_id

            existing.user_id = user_id

            existing.device_name = device_name

            existing.platform = platform

            existing.status = "ACTIVE"

            existing.last_seen_at = datetime.utcnow()

            self.db.commit()

            return existing

        device = SyncDeviceModel(

            merchant_id=merchant_id,

            device_id=device_id,

            branch_id=branch_id,

            user_id=user_id,

            device_name=device_name,

            platform=platform,

            status="ACTIVE",

            last_seen_at=datetime.utcnow()

        )

        self.db.add(
            device
        )

        self.db.commit()

        self.db.refresh(
            device
        )

        return device

    def touch_device(

        self,

        merchant_id: str,

        device_id: str

    ):

        device = (

            self.db.query(
                SyncDeviceModel
            )

            .filter(
                SyncDeviceModel.merchant_id
                == merchant_id,

                SyncDeviceModel.device_id
                == device_id

            )

            .first()

        )

        if device:

            device.last_seen_at = datetime.utcnow()

            self.db.commit()

        return device

    def record_client_event(

        self,

        merchant_id: str,

        device_id: str,

        client_event_id: str,

        idempotency_key: str,

        command_name: str,

        payload: dict,

        branch_id: str | None = None,

        expected_version: int | None = None,

        occurred_at=None

    ):

        record = SyncInboxEventModel(

            merchant_id=merchant_id,

            branch_id=branch_id,

            device_id=device_id,

            client_event_id=client_event_id,

            idempotency_key=idempotency_key,

            command_name=command_name,

            payload=payload,

            expected_version=expected_version,

            status="RECEIVED",

            occurred_at=occurred_at

        )

        self.db.add(
            record
        )

        try:

            self.db.commit()

            self.db.refresh(
                record
            )

            return record, False

        except IntegrityError:

            self.db.rollback()

            existing = (

                self.db.query(
                    SyncInboxEventModel
                )

                .filter(
                    SyncInboxEventModel.merchant_id
                    == merchant_id,

                    SyncInboxEventModel.device_id
                    == device_id,

                    SyncInboxEventModel.client_event_id
                    == client_event_id

                )

                .first()

            )

            return existing, True

    def pull_server_events(

        self,

        merchant_id: str,

        after_event_id: int = 0,

        limit: int = 100

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.merchant_id
                == merchant_id,

                EventModel.id > after_event_id

            )

            .order_by(
                EventModel.id.asc()
            )

            .limit(
                limit
            )

            .all()

        )

    def get_device_status(

        self,

        merchant_id: str,

        device_id: str

    ):

        received_count = (

            self.db.query(
                SyncInboxEventModel
            )

            .filter(
                SyncInboxEventModel.merchant_id
                == merchant_id,

                SyncInboxEventModel.device_id
                == device_id

            )

            .count()

        )

        pending_count = (

            self.db.query(
                SyncInboxEventModel
            )

            .filter(
                SyncInboxEventModel.merchant_id
                == merchant_id,

                SyncInboxEventModel.device_id
                == device_id,

                SyncInboxEventModel.status.in_(

                    [
                        "RECEIVED",
                        "PENDING"
                    ]

                )

            )

            .count()

        )

        failed_count = (

            self.db.query(
                SyncInboxEventModel
            )

            .filter(
                SyncInboxEventModel.merchant_id
                == merchant_id,

                SyncInboxEventModel.device_id
                == device_id,

                SyncInboxEventModel.status
                == "FAILED"

            )

            .count()

        )

        return {

            "merchant_id":
                merchant_id,

            "device_id":
                device_id,

            "pending_count":
                pending_count,

            "failed_count":
                failed_count,

            "received_count":
                received_count

        }