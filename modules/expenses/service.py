import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def record_expense(

    merchant_id: str,

    category: str,

    amount: float,

    notes: str,

    previous_hash: str

):

    payload = {

        "expense_id":

            str(uuid.uuid4()),

        "category":

            category,

        "amount":

            amount,

        "notes":

            notes

    }

    return create_event(

        EventType.EXPENSE_RECORDED,

        merchant_id,

        payload,

        previous_hash

    )