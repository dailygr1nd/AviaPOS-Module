from sqlalchemy.orm import Session

from infrastructure.event_store.models import (
    EventModel
)


class EventRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def append(

        self,

        event,

        commit: bool = True

    ):

        model = EventModel(

            event_id=event.event_id,

            event_type=event.event_type,

            merchant_id=event.merchant_id,

            aggregate_id=event.aggregate_id,

            version=event.version,

            payload=event.payload,

            previous_hash=event.previous_hash,

            current_hash=event.current_hash

        )

        self.db.add(
            model
        )

        if commit:

            try:

                self.db.commit()

                self.db.refresh(
                    model
                )

            except Exception:

                self.db.rollback()

                raise

        else:

            self.db.flush()

        return model

    def get_latest_hash(

        self,

        merchant_id: str

    ) -> str:

        latest = (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.merchant_id
                == merchant_id
            )

            .order_by(
                EventModel.id.desc()
            )

            .first()

        )

        if not latest:

            return "GENESIS"

        return latest.current_hash

    def get_after(

        self,

        event_id: int

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.id > event_id
            )

            .order_by(
                EventModel.id.asc()
            )

            .all()

        )

    def get_after_id(

        self,

        last_event_id: int,

        limit: int = 1000

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.id > last_event_id
            )

            .order_by(
                EventModel.id.asc()
            )

            .limit(
                limit
            )

            .all()

        )

    def get_events_after_version(

        self,

        aggregate_id: str,

        version: int

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.aggregate_id
                == aggregate_id,

                EventModel.version
                > version
            )

            .order_by(
                EventModel.version.asc()
            )

            .all()

        )