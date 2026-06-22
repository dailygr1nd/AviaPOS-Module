from core.events.bus import (
    event_bus
)

from modules.inventory.handlers import (
    inventory_event_handler
)

from modules.sales.handlers import (
    sales_event_handler
)


def register_handlers():

    inventory_events = [

        "INVENTORY_RECEIVED",

        "INVENTORY_DEDUCTED",

        "INVENTORY_ADJUSTED"

    ]

    for event_type in inventory_events:

        event_bus.subscribe(

            event_type,

            inventory_event_handler

        )

    sales_events = [

        "SALE_CREATED",

        "SALE_COMPLETED"

    ]

    for event_type in sales_events:

        event_bus.subscribe(

            event_type,

            sales_event_handler

        )