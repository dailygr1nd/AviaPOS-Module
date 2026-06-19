# modules/products/projection.py

products = {}

from core.events.types import (
    EventType
)

from modules.products.projection import (
    products
)


def apply_event(event):

    payload = (
        event["payload"]
    )

    event_type = (
        event["event_type"]
    )

    if (
        event_type ==
        EventType.PRODUCT_CREATED.value
    ):

        products[
            payload["product_id"]
        ] = {

            "sku":
            payload["sku"],

            "name":
            payload["name"],

            "selling_price":
            payload["selling_price"],

            "cost_price":
            payload["cost_price"]
        }

    elif (
        event_type ==
        EventType.PRODUCT_PRICE_UPDATED.value
    ):

        products[
            payload["product_id"]
        ][
            "selling_price"
        ] = payload[
            "selling_price"
        ]


        