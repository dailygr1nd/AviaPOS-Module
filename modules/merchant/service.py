import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def create_merchant(

    merchant_name: str,

    owner_name: str,

    phone: str,

    email: str,

    previous_hash: str = "GENESIS"

):

    merchant_id = str(
        uuid.uuid4()
    )

    payload = {

        "merchant_id":
            merchant_id,

        "merchant_name":
            merchant_name,

        "owner_name":
            owner_name,

        "phone":
            phone,

        "email":
            email
    }

    event = create_event(

        EventType.MERCHANT_CREATED,

        merchant_id,

        payload,

        previous_hash
    )

    return merchant_id, event