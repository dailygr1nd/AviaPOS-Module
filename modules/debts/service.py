import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_debt(

    merchant_id: str,

    customer_id: str,

    amount: float,

    currency: str,

    due_date: str,

    previous_hash: str

):

    payload = {

        "debt_id": str(
            uuid.uuid4()
        ),

        "customer_id": customer_id,

        "amount": amount,

        "currency": currency,

        "due_date": due_date

    }

    return create_event(

        EventType.DEBT_CREATED,

        merchant_id,

        payload,

        previous_hash
    )


def settle_debt(

    merchant_id: str,

    debt_id: str,

    customer_id: str,

    amount: float,

    currency: str,

    previous_hash: str

):

    payload = {

        "debt_id": debt_id,

        "customer_id": customer_id,

        "amount": amount,

        "currency": currency

    }

    return create_event(

        EventType.DEBT_SETTLED,

        merchant_id,

        payload,

        previous_hash
    )