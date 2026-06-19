import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_supplier(

    merchant_id: str,

    name: str,

    phone: str,

    previous_hash: str

):

    payload = {

        "supplier_id":

            str(uuid.uuid4()),

        "name":

            name,

        "phone":

            phone

    }

    return create_event(

        EventType.SUPPLIER_CREATED,

        merchant_id,

        payload,

        previous_hash

    )