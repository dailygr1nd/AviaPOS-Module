from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from infrastructure.event_store.models import (
    EventModel
)

from infrastructure.concurrency.exceptions import (
    OptimisticConcurrencyError
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

        try:

            if commit:

                self.db.commit()

                self.db.refresh(
                    model
                )

            else:

                self.db.flush()

        except IntegrityError as exc:

            self.db.rollback()

            raise OptimisticConcurrencyError(

                "Concurrency conflict: aggregate version already exists."

            ) from exc

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

    def get_latest_version(

        self,

        merchant_id: str,

        aggregate_id: str

    ) -> int:

        latest = (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.merchant_id
                == merchant_id,

                EventModel.aggregate_id
                == aggregate_id

            )

            .order_by(
                EventModel.version.desc()
            )

            .first()

        )

        if not latest:

            return 0

        return latest.version

    def assert_expected_version(

        self,

        merchant_id: str,

        aggregate_id: str,

        expected_version: int

    ):

        actual_version = self.get_latest_version(

            merchant_id,

            aggregate_id

        )

        if actual_version != expected_version:

            raise OptimisticConcurrencyError(

                f"Concurrency conflict for aggregate "

                f"{aggregate_id}. Expected version "

                f"{expected_version}, but current version is "

                f"{actual_version}."

            )

        return actual_version

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

    def get_by_merchant_ordered(

        self,

        merchant_id: str

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.merchant_id
                == merchant_id
            )

            .order_by(
                EventModel.id.asc()
            )

            .all()

        )

    def get_by_aggregate_ordered(

        self,

        merchant_id: str,

        aggregate_id: str

    ):

        return (

            self.db.query(
                EventModel
            )

            .filter(
                EventModel.merchant_id
                == merchant_id,

                EventModel.aggregate_id
                == aggregate_id

            )

            .order_by(
                EventModel.version.asc()
            )

            .all()

        )