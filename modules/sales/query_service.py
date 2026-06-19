from core.ledger.repository import (
    get_all_events
)

from modules.sales.projector import (
    apply_event
)

from modules.sales.projection import (
    sales
)


def rebuild():

    sales.clear()

    for event in get_all_events():

        apply_event(event)

    return sales


def get_sale(
    sale_id: str
):

    projection = (
        rebuild()
    )

    return projection.get(
        sale_id
    )