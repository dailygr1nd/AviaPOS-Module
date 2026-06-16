import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def create_branch_transfer(

    merchant_id,

    source_branch,

    destination_branch,

    amount,

    currency,

    previous_hash

):

    payload = {

        "transfer_id":
            str(uuid.uuid4()),

        "source_branch":
            source_branch,

        "destination_branch":
            destination_branch,

        "amount":
            amount,

        "currency":
            currency
    }

    return create_event(

        EventType.BRANCH_TRANSFER_CREATED,

        merchant_id,

        payload,

        previous_hash
    )

