import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def create_branch(

    merchant_id,

    branch_name,

    location,

    previous_hash

):

    payload = {

        "branch_id":

            str(uuid.uuid4()),

        "branch_name":

            branch_name,

        "location":

            location
    }

    return create_event(

        EventType.BRANCH_CREATED,

        merchant_id,

        payload,

        previous_hash
    )