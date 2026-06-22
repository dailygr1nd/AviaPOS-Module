from sqlalchemy.orm import Session

from infrastructure.event_store.models import (
    EventModel
)


class EventRepository:

    def __init__(self, db: Session):
        self.db = db

    def append(self, event):

        from infrastructure.redis.streams import (
    publish_event
    )

        model = EventModel(

            event_id=event.event_id,

            event_type=event.event_type,

            merchant_id=event.merchant_id,

            aggregate_id=event.aggregate_id,

            payload=event.payload,

            previous_hash=event.previous_hash,

            current_hash=event.current_hash

        )

        self.db.add(model)

        self.db.commit()
        
        publish_event(event)

        self.db.refresh(model)

        return model

    def get_after(

        self,

        event_id: int

    ):

        return (

            self.db.query(EventModel)

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
            EventModel.id >
            last_event_id
        )

        .order_by(
            EventModel.id.asc()
        )

        .limit(limit)

        .all()

    )