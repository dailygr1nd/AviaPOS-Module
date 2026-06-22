import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.event_store.repository import (
    EventRepository
)


def create_receivable(

    merchant_id: str,

    branch_id: str,

    customer_id: str,

    sale_id: str,

    amount: float

):

    receivable_id = str(
        uuid.uuid4()
    )

    payload = {

        "receivable_id":
            receivable_id,

        "merchant_id":
            merchant_id,

        "branch_id":
            branch_id,

        "customer_id":
            customer_id,

        "sale_id":
            sale_id,

        "amount":
            amount

    }

    event = create_event(

        EventType.RECEIVABLE_CREATED,

        merchant_id,

        payload

    )

    db = SessionLocal()

    EventRepository(
        db
    ).append(
        event
    )

    return event


def record_payment(

    receivable_id: str,

    merchant_id: str,

    amount: float,

    payment_method: str

):

    payload = {

        "receivable_id":
            receivable_id,

        "amount":
            amount,

        "payment_method":
            payment_method

    }

    event = create_event(

        EventType.RECEIVABLE_PAYMENT_RECORDED,

        merchant_id,

        payload

    )

    db = SessionLocal()

    EventRepository(
        db
    ).append(
        event
    )

    return event