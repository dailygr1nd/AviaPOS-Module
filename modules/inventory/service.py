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

from modules.inventory.aggregate import (
    InventoryAggregate
)


def receive_stock(

    merchant_id: str,

    product_id: str,

    sku: str,

    quantity: int,

    cost_price: float

):

    inventory = (
        InventoryAggregate(
            product_id
        )
    )

    inventory.validate_receipt(
        quantity
    )

    payload = {

        "product_id": product_id,

        "sku": sku,

        "quantity": quantity,

        "cost_price": cost_price

    }

    event = create_event(

        EventType
        .INVENTORY_RECEIVED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(
        event
    )

    return event


def deduct_stock(

    merchant_id: str,

    product_id: str,

    sku: str,

    quantity: int,

    reason: str

):

    inventory = (
        InventoryAggregate(
            product_id
        )
    )

    inventory.validate_deduction(
        quantity
    )

    payload = {

        "product_id": product_id,

        "sku": sku,

        "quantity": quantity,

        "reason": reason

    }

    event = create_event(

        EventType
        .INVENTORY_DEDUCTED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(
        event
    )

    return event


def adjust_stock(

    merchant_id: str,

    product_id: str,

    sku: str,

    adjustment: int,

    reason: str

):

    inventory = (
        InventoryAggregate(
            product_id
        )
    )

    inventory.validate_adjustment(
        adjustment
    )

    payload = {

        "product_id": product_id,

        "sku": sku,

        "adjustment": adjustment,

        "reason": reason

    }

    event = create_event(

        EventType
        .INVENTORY_ADJUSTED,

        merchant_id,

        payload,

        get_last_event_hash()

    )

    append_event(
        event
    )

    return event