import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)


def create_sale(

    merchant_id: str,

    product_id: str,

    quantity: int,

    amount: float,

    currency: str,

    previous_hash: str

):

    payload = {

        "sale_id": str(
            uuid.uuid4()
        ),

        "product_id":
            product_id,

        "quantity":
            quantity,

        "amount":
            amount,

        "currency":
            currency

    }

    return create_event(

        EventType.SALE_CREATED,

        merchant_id,

        payload,

        previous_hash

    )