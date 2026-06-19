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

from modules.customers.aggregate import (
    CustomerAggregate
)


def create_customer(

    merchant_id: str,

    customer_id: str,

    name: str,

    phone: str = ""

):

    CustomerAggregate.validate_create(
        name
    )

    payload = {

        "customer_id":
            customer_id,

        "name":
            name,

        "phone":
            phone

    }

    event = create_event(

        EventType
        .CUSTOMER_CREATED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(event)

    return event