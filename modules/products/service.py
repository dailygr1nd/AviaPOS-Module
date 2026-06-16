import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def create_product(

    merchant_id,

    sku,

    name,

    category,

    unit_price,

    previous_hash

):

    payload = {

        "product_id":
            str(uuid.uuid4()),

        "sku":
            sku,

        "name":
            name,

        "category":
            category,

        "unit_price":
            unit_price
    }

    return create_event(

        EventType.PRODUCT_CREATED,

        merchant_id,

        payload,

        previous_hash
    )