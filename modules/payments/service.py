import uuid

from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.event_store.repository import (
    EventRepository
)

from core.ledger.event_factory import (
    create_event
)

from core.events.types import (
    EventType
)


def create_payment(

    merchant_id: str,

    amount: float,

    payment_method: str,

    reference_type: str,

    reference_id: str

):

    payment_id = str(
        uuid.uuid4()
    )

    payload = {

        "payment_id":
            payment_id,

        "merchant_id":
            merchant_id,

        "amount":
            amount,

        "payment_method":
            payment_method,

        "reference_type":
            reference_type,

        "reference_id":
            reference_id

    }

    event = create_event(

        EventType.PAYMENT_CREATED,

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


def complete_payment(

    payment_id: str,

    merchant_id: str

):

    payload = {

        "payment_id":
            payment_id

    }

    event = create_event(

        EventType.PAYMENT_COMPLETED,

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


def fail_payment(

    payment_id: str,

    merchant_id: str

):

    payload = {

        "payment_id":
            payment_id

    }

    event = create_event(

        EventType.PAYMENT_FAILED,

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