from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def receive_stock(

    merchant_id: str,

    product_id: str,

    sku: str,

    quantity: int,

    cost_price: float,

    previous_hash: str

):

    payload = {

        "product_id": product_id,

        "sku": sku,

        "quantity": quantity,

        "cost_price": cost_price

    }

    return create_event(

        EventType.INVENTORY_RECEIVED,

        merchant_id,

        payload,

        previous_hash

    )