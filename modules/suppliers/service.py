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


def create_supplier(

    merchant_id: str,

    supplier_id: str,

    name: str,

    phone: str = ""

):

    payload = {

        "supplier_id":
            supplier_id,

        "name":
            name,

        "phone":
            phone

    }

    event = create_event(

        EventType.SUPPLIER_CREATED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(
        event
    )

    return event