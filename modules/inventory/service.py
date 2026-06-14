from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def receive_stock(

    merchant_id: str,

    sku: str,

    quantity: int,

    previous_hash: str

):

    payload = {

        "sku":
            sku,

        "quantity":
            quantity
    }

    return create_event(

        EventType.STOCK_RECEIVED,

        merchant_id,

        payload,

        previous_hash
    )


def deduct_stock(

    merchant_id: str,

    sku: str,

    quantity: int,

    reason: str,

    previous_hash: str

):

    payload = {

        "sku":
            sku,

        "quantity":
            quantity,

        "reason":
            reason
    }

    return create_event(

        EventType.STOCK_DEDUCTED,

        merchant_id,

        payload,

        previous_hash
    )