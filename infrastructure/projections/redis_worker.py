import json

from infrastructure.redis.client import (
    redis_client
)

from infrastructure.redis.consumer import (

    GROUP_NAME,

    CONSUMER_NAME,

    EVENT_STREAM

)

from infrastructure.database.session import (
    SessionLocal
)

from modules.inventory.projector import (
    InventoryProjector
)


from modules.expenses.projector import (
    ExpenseProjector
)

expense_projector = (
    ExpenseProjector(db)
)


def start_projection_worker():


    expense_projector.handle(
    event
    )

    db = SessionLocal()

    inventory_projector = (
        InventoryProjector(db)
    )

    while True:

        messages = (

            redis_client.xreadgroup(

                GROUP_NAME,

                CONSUMER_NAME,

                {

                    EVENT_STREAM: ">"

                },

                count=10,

                block=5000

            )

        )

        for _, records in messages:

            for msg_id, data in records:

                event_type = data[
                    "event_type"
                ]

                payload = eval(
                    data["payload"]
                )

                class Event:
                    pass

                event = Event()

                event.event_type = (
                    event_type
                )

                event.payload = payload

                inventory_projector.handle(
                    event
                )

                redis_client.xack(

                    EVENT_STREAM,

                    GROUP_NAME,

                    msg_id

                )