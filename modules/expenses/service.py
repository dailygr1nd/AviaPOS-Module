from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

def record_expense(

    merchant_id,

    category,

    amount,

    currency,

    description,

    previous_hash

):

    payload = {

        "category":
            category,

        "amount":
            amount,

        "currency":
            currency,

        "description":
            description
    }

    return create_event(

        EventType.EXPENSE_RECORDED,

        merchant_id,

        payload,

        previous_hash
    )