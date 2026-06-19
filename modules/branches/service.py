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


def create_branch(

    merchant_id: str,

    branch_id: str,

    name: str,

    location: str

):

    payload = {

        "branch_id":
            branch_id,

        "name":
            name,

        "location":
            location

    }

    event = create_event(

        EventType.BRANCH_CREATED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(
        event
    )

    return event