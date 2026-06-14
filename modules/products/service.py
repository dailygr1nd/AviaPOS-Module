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

    selling_price: float,

    cost_price: float,

    unit: str,

    previous_hash: str

):

    payload = {

        "product_id":
            str(uuid.uuid4()),

        "sku":
            sku,

        "name":
            name,

        "selling_price":
            selling_price,

        "cost_price":
            cost_price,

        "unit":
            unit
    }

    return create_event(

        EventType.PRODUCT_CREATED,

        merchant_id,

        payload,

        previous_hash
    )