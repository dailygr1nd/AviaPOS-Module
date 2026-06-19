from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

from core.ledger.store import (
    append_event
)

from core.ledger.hash_chain import (
    get_last_event_hash
)

from modules.products.aggregate import (
    ProductAggregate
)


def create_product(

    merchant_id: str,

    product_id: str,

    sku: str,

    name: str,

    selling_price: float,

    cost_price: float

):

    ProductAggregate.validate_create(

        name=name,

        sku=sku

    )

    payload = {

        "product_id": product_id,

        "sku": sku,

        "name": name,

        "selling_price":
            selling_price,

        "cost_price":
            cost_price

    }

    event = create_event(

        EventType
        .PRODUCT_CREATED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(event)

    return event