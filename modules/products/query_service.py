from core.ledger.repository import (
    get_all_events
)

from modules.products.projection import (
    products
)

from modules.products.projection import (
    apply_event
)


def rebuild():

    products.clear()

    for event in get_all_events():

        apply_event(event)

    return products


def get_product(
    product_id: str
):

    projection = rebuild()

    return projection.get(
        product_id
    )