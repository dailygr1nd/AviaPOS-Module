from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_customer(

    merchant_id: str,

    customer_id: str,

    name: str,

    phone: str,

    previous_hash: str

):

    payload = {

        "customer_id": customer_id,

        "name": name,

        "phone": phone

    }

    return create_event(

        EventType.CUSTOMER_CREATED,

        merchant_id,

        payload,

        previous_hash
    )