import uuid

from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.outbox.models import (
    OutboxMessageModel
)


class OutboxRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def add_event(

        self,

        event,

        persisted_event_id: int

    ):

        message = OutboxMessageModel(

            message_id=str(
                uuid.uuid4()
            ),

            event_id=event.event_id,

            event_type=event.event_type,

            merchant_id=event.merchant_id,

            aggregate_id=event.aggregate_id,

            payload={

                "persisted_event_id":
                    persisted_event_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "merchant_id":
                    event.merchant_id,

                "aggregate_id":
                    event.aggregate_id,

                "version":
                    event.version,

                "previous_hash":
                    event.previous_hash,

                "current_hash":
                    event.current_hash,

                "payload":
                    event.payload

            },

            status="PENDING",

            attempts=0

        )

        self.db.add(
            message
        )

        self.db.flush()

        return message

    def get_pending(

        self,

        limit: int = 100

    ):

        return (

            self.db.query(
                OutboxMessageModel
            )

            .filter(
                OutboxMessageModel.status
                == "PENDING"
            )

            .order_by(
                OutboxMessageModel.id.asc()
            )

            .with_for_update(
                skip_locked=True
            )

            .limit(
                limit
            )

            .all()

        )

    def mark_published(

        self,

        message: OutboxMessageModel

    ):

        message.status = "PUBLISHED"

        message.published_at = datetime.utcnow()

        self.db.flush()

    def mark_failed(

        self,

        message: OutboxMessageModel,

        error: Exception

    ):

        message.attempts += 1

        message.last_error = str(
            error
        )

        if message.attempts >= 5:

            message.status = "FAILED"

        self.db.flush()