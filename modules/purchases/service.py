import uuid

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

from modules.purchases.aggregate import (
    PurchaseAggregate
)

from modules.inventory.service import (
    receive_stock
)


def create_purchase_order(

    merchant_id: str,

    supplier_id: str,

    items: list

):

    purchase_id = str(
        uuid.uuid4()
    )

    aggregate = (
        PurchaseAggregate()
    )

    po_event = create_event(

        EventType
        .PURCHASE_ORDER_CREATED,

        merchant_id,

        {

            "purchase_id":
                purchase_id,

            "supplier_id":
                supplier_id

        },

        get_last_event_hash()

    )

    append_event(
        po_event
    )

    for item in items:

        aggregate.add_line(

            product_id=
                item[
                    "product_id"
                ],

            sku=
                item[
                    "sku"
                ],

            quantity=
                item[
                    "quantity"
                ],

            cost_price=
                item[
                    "cost_price"
                ]

        )

    return {

        "purchase_id":
            purchase_id,

        "total":
            aggregate.total

    }

def receive_purchase(

    merchant_id: str,

    purchase_id: str,

    items: list

):

    receipt_event = create_event(

        EventType
        .PURCHASE_RECEIVED,

        merchant_id,

        {

            "purchase_id":
                purchase_id

        },

        get_last_event_hash()

    )

    append_event(
        receipt_event
    )

    for item in items:

        receive_stock(

            merchant_id=
                merchant_id,

            product_id=
                item[
                    "product_id"
                ],

            sku=
                item[
                    "sku"
                ],

            quantity=
                item[
                    "quantity"
                ],

            cost_price=
                item[
                    "cost_price"
                ]
        )

    return receipt_event