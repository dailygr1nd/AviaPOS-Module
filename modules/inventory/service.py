from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def receive_stock(

    merchant_id,

    product_id,

    quantity,

    unit_cost,

    previous_hash

):

    payload = {

        "product_id":
            product_id,

        "quantity":
            quantity,

        "unit_cost":
            unit_cost
    }

    return create_event(

        EventType.STOCK_RECEIVED,

        merchant_id,

        payload,

        previous_hash
    )

def deduct_stock(

    merchant_id,

    product_id,

    quantity,

    previous_hash

):

    payload = {

        "product_id":
            product_id,

        "quantity":
            quantity
    }

    return create_event(

        EventType.STOCK_DEDUCTED,

        merchant_id,

        payload,

        previous_hash
    )