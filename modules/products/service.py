import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_product(

    merchant_id: str,

    sku: str,

    name: str,

    price: float,

    previous_hash: str

):

    payload = {

        "product_id":

            sku,

        "sku":

            sku,

        "name":

            name,

        "price":

            price

    }

    return create_event(

        EventType.PRODUCT_CREATED,

        merchant_id,

        payload,

        previous_hash

    )