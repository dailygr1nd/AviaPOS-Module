import uuid

from datetime import datetime

from core.events.base import Event

from core.events.hash import (
    calculate_payload_hash
)


def create_event(

    event_type,

    merchant_id,

    payload,

    event_hash,

    previous_hash

):

    return Event(

        event_id=str(
            uuid.uuid4()
        ),

        event_type=str(
            event_type
        ),

        merchant_id=merchant_id,

        timestamp=datetime.utcnow()
        .isoformat(),

        event_hash=event_hash,

        previous_hash=previous_hash,

        payload_hash=
            calculate_payload_hash(
                payload
            ),

        payload=payload
    )