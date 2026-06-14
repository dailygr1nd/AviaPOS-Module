from modules.inventory.service import (
    receive_stock
)

from storage.sqlite.sqlite.event_store import (
    EventStore
)


store = EventStore(
    "aviapos.db"
)

event = receive_stock(

    merchant_id="M001",

    sku="CEMENT001",

    quantity=100,

    previous_hash="GENESIS"
)

store.append(event)

print(event)