from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_sale(

    merchant_id: str,

    amount: float,

    currency: str,

    items: list,

    payment_method: str,

    previous_hash: str

):

    payload = {

        "amount":
            amount,

        "currency":
            currency,

        "items":
            items,

        "payment_method":
            payment_method
    }

    return create_event(

        EventType.SALE_CREATED,

        merchant_id,

        payload,

        previous_hash
    )