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

from modules.debts.aggregate import (
    DebtAggregate
)


def create_debt(

    merchant_id: str,

    debt_id: str,

    customer_id: str,

    sale_id: str,

    amount: float

):

    DebtAggregate.validate_amount(
        amount
    )

    payload = {

        "debt_id":
            debt_id,

        "customer_id":
            customer_id,

        "sale_id":
            sale_id,

        "amount":
            amount

    }

    event = create_event(

        EventType
        .DEBT_CREATED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(event)

    return event


def record_payment(

    merchant_id: str,

    debt_id: str,

    amount: float,

    method: str

):

    payload = {

        "debt_id":
            debt_id,

        "amount":
            amount,

        "method":
            method

    }

    event = create_event(

        EventType
        .DEBT_PAYMENT_RECEIVED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(event)

    return event