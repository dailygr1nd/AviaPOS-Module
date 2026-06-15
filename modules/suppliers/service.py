import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def create_supplier(

    merchant_id,

    supplier_name,

    phone,

    previous_hash

):

    payload = {

        "supplier_id":
            str(uuid.uuid4()),

        "supplier_name":
            supplier_name,

        "phone":
            phone
    }

    return create_event(

        EventType.SUPPLIER_CREATED,

        merchant_id,

        payload,

        previous_hash
    )