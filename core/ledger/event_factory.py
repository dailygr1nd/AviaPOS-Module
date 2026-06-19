import uuid

from datetime import datetime

from core.events.base import Event

from core.events.hash import (
    calculate_event_hash,
    calculate_payload_hash
)


def create_event(
    event_type,
    merchant_id,
    payload,
    previous_hash
):

    payload_hash = calculate_payload_hash(
        payload
    )

    event_hash = calculate_event_hash(
        str(event_type),
        merchant_id,
        payload_hash,
        previous_hash
    )

    return Event(

        event_id=str(
            uuid.uuid4()
        ),

        event_type=event_type.value,

        merchant_id=merchant_id,

        timestamp=datetime.utcnow()
        .isoformat(),

        previous_hash=previous_hash,

        payload_hash=payload_hash,

        event_hash=event_hash,

        payload=payload

    )