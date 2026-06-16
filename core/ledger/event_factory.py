import uuid

from datetime import (
    datetime,
    timezone
)

from core.events.base import (
    Event
)

from core.events.hash import (
    calculate_payload_hash
)

from core.events.event_hash import (
    calculate_event_hash
)

def create_event(

    event_type,

    merchant_id,

    payload,

    previous_hash="GENESIS"

):
        timestamp = (

        datetime.now(
            timezone.utc
        ).isoformat()

    )
        payload_hash = (

        calculate_payload_hash(
            payload
        )

    )
        event_hash = (

        calculate_event_hash(

            str(event_type),

            merchant_id,

            timestamp,

            previous_hash,

            payload_hash

        )

    )
        return Event(

        event_id=str(
            uuid.uuid4()
        ),

        event_type=str(
            event_type
        ),

        merchant_id=
            merchant_id,

        timestamp=
            timestamp,

        previous_hash=
            previous_hash,

        payload_hash=
            payload_hash,

        event_hash=
            event_hash,

        payload=
            payload
    )