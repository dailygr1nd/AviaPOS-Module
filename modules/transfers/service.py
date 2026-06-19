import uuid

from core.events.types import EventType

from core.ledger.event_factory import create_event

from core.ledger.store import append_event

from core.ledger.hash_chain import get_last_event_hash

from modules.inventory.service import (
    deduct_stock,
    receive_stock
)


def create_transfer(

    merchant_id: str,

    source_branch_id: str,

    destination_branch_id: str,

    product_id: str,

    sku: str,

    quantity: int

):

    transfer_id = str(uuid.uuid4())

    event = create_event(

        EventType.BRANCH_TRANSFER_CREATED,

        merchant_id,

        {

            "transfer_id": transfer_id,
            "source_branch_id": source_branch_id,
            "destination_branch_id": destination_branch_id,
            "product_id": product_id,
            "sku": sku,
            "quantity": quantity

        },

        get_last_event_hash()

    )

    append_event(event)

    deduct_stock(

        merchant_id=merchant_id,
        branch_id=source_branch_id,
        product_id=product_id,
        sku=sku,
        quantity=quantity,
        reason="TRANSFER_OUT"

    )

    receive_stock(

        merchant_id=merchant_id,
        branch_id=destination_branch_id,
        product_id=product_id,
        sku=sku,
        quantity=quantity,
        cost_price=0

    )

    return {
        "transfer_id": transfer_id
    }


def settle_transfer(

    merchant_id: str,

    transfer_id: str

):

    event = create_event(

        EventType.BRANCH_TRANSFER_SETTLED,

        merchant_id,

        {

            "transfer_id": transfer_id

        },

        get_last_event_hash()

    )

    append_event(event)

    return {
        "transfer_id": transfer_id,
        "status": "SETTLED"
    }