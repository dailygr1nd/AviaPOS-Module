from core.ledger.repository import (
    get_all_events
)

from modules.customers.projection import (
    customers
)

from modules.customers.projector import (
    apply_event
)


def rebuild():

    customers.clear()

    for event in get_all_events():

        apply_event(event)

    return customers


def get_customer(
    customer_id: str
):

    projection = rebuild()

    return projection.get(
        customer_id
    )