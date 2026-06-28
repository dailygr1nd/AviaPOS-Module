import json

from types import SimpleNamespace

from infrastructure.redis.client import (
    redis_client
)

from infrastructure.redis.consumer import (
    EVENT_STREAM,
    REACTION_CONSUMER_NAME,
    REACTION_GROUP_NAME
)

from modules.sales.reactions import (
    SaleCompletedReaction
)


def _build_event(
    data: dict
):

    return SimpleNamespace(

        persisted_event_id=
            data.get(
                "persisted_event_id"
            ),

        event_id=
            data.get(
                "event_id"
            ),

        event_type=
            data.get(
                "event_type"
            ),

        merchant_id=
            data.get(
                "merchant_id"
            ),

        aggregate_id=
            data.get(
                "aggregate_id"
            ),

        version=
            int(
                data.get(
                    "version",
                    1
                )
            ),

        previous_hash=
            data.get(
                "previous_hash"
            ),

        current_hash=
            data.get(
                "current_hash"
            ),

        payload=
            json.loads(
                data.get(
                    "payload",
                    "{}"
                )
            )

    )


def start_sales_reaction_worker():

    reaction = SaleCompletedReaction()

    while True:

        messages = redis_client.xreadgroup(

            REACTION_GROUP_NAME,

            REACTION_CONSUMER_NAME,

            {
                EVENT_STREAM: ">"
            },

            count=10,

            block=5000

        )

        if not messages:

            continue

        for _, records in messages:

            for msg_id, data in records:

                event = _build_event(
                    data
                )

                try:

                    reaction.handle(
                        event
                    )

                    redis_client.xack(

                        EVENT_STREAM,

                        REACTION_GROUP_NAME,

                        msg_id

                    )

                except Exception as exc:

                    print(

                        f"Sales reaction failed for "

                        f"{event.event_id}: {exc}"

                    )