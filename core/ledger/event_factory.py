import uuid

from datetime import datetime

from core.events.base import Event

from core.events.hash import (
    calculate_event_hash,
    calculate_payload_hash
)


AGGREGATE_ID_KEYS = [

    "payment_id",

    "expense_id",

    "receivable_id",

    "payable_id",

    "sale_id",

    "product_id",

    "branch_id",

    "customer_id",

    "supplier_id",

    "transfer_id",

    "merchant_id"

]


def _event_type_value(event_type) -> str:

    if hasattr(
        event_type,
        "value"
    ):

        return event_type.value

    return str(
        event_type
    )


def _infer_aggregate_id(
    payload: dict,
    merchant_id: str
) -> str:

    for key in AGGREGATE_ID_KEYS:

        value = payload.get(
            key
        )

        if value:

            return str(
                value
            )

    return merchant_id


def create_event(

    event_type,

    merchant_id: str,

    payload: dict,

    previous_hash: str = "GENESIS",

    aggregate_id: str | None = None,

    version: int = 1,

    metadata: dict | None = None

):

    event_type_value = _event_type_value(
        event_type
    )

    resolved_aggregate_id = (

        aggregate_id

        or

        _infer_aggregate_id(
            payload,
            merchant_id
        )

    )

    payload_hash = calculate_payload_hash(
        payload
    )

    event_hash = calculate_event_hash(

        event_type_value,

        merchant_id,

        payload_hash,

        previous_hash

    )

    return Event(

        event_id=str(
            uuid.uuid4()
        ),

        event_type=event_type_value,

        merchant_id=merchant_id,

        timestamp=datetime.utcnow()
        .isoformat(),

        previous_hash=previous_hash,

        payload_hash=payload_hash,

        event_hash=event_hash,

        payload=payload,

        aggregate_id=resolved_aggregate_id,

        version=version,

        metadata=metadata or {}

    )