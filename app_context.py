from core.events.event_bus import (
    EventBus
)

from storage.sqlite.event_store import (
    EventStore
)

store = EventStore(
    "aviapos.db"
)

event_bus = EventBus()

from core.events.event_handlers import (

    handle_sale_created,

    handle_debt_created,

    handle_stock_received,

    handle_stock_deducted

)

event_bus.subscribe(

    "SALE_CREATED",

    handle_sale_created

)

event_bus.subscribe(

    "DEBT_CREATED",

    handle_debt_created

)

event_bus.subscribe(

    "STOCK_RECEIVED",

    handle_stock_received

)

event_bus.subscribe(

    "STOCK_DEDUCTED",

    handle_stock_deducted

)