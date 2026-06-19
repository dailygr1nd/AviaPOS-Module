from storage.sqlite.event_store import (
    EventStore
)

from core.events.event_bus import (
    EventBus
)


store = EventStore(

    "storage/sqlite/aviapos.db"

)

event_bus = EventBus()