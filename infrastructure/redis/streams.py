import json

from infrastructure.redis.client import (
    redis_client
)


EVENT_STREAM = "aviapos_events"


def publish_outbox_message(
    message_payload: dict
):

    redis_payload = {

        "persisted_event_id":
            str(
                message_payload[
                    "persisted_event_id"
                ]
            ),

        "event_id":
            str(
                message_payload[
                    "event_id"
                ]
            ),

        "event_type":
            str(
                message_payload[
                    "event_type"
                ]
            ),

        "merchant_id":
            str(
                message_payload[
                    "merchant_id"
                ]
            ),

        "aggregate_id":
            str(
                message_payload[
                    "aggregate_id"
                ]
            ),

        "version":
            str(
                message_payload.get(
                    "version",
                    1
                )
            ),

        "previous_hash":
            str(
                message_payload[
                    "previous_hash"
                ]
            ),

        "current_hash":
            str(
                message_payload[
                    "current_hash"
                ]
            ),

        "payload":
            json.dumps(
                message_payload[
                    "payload"
                ],
                default=str
            )

    }

    return redis_client.xadd(

        EVENT_STREAM,

        redis_payload

    )


def publish_event(
    event
):

    """
    Compatibility helper.

    New write flows should not call this directly.
    New write flows must use:

        Event Store
        +
        Outbox
        +
        Outbox Publisher

    This remains only for temporary legacy compatibility.
    """

    return redis_client.xadd(

        EVENT_STREAM,

        {

            "persisted_event_id":
                "",

            "event_id":
                str(
                    event.event_id
                ),

            "event_type":
                str(
                    event.event_type
                ),

            "merchant_id":
                str(
                    event.merchant_id
                ),

            "aggregate_id":
                str(
                    event.aggregate_id
                ),

            "version":
                str(
                    event.version
                ),

            "previous_hash":
                str(
                    event.previous_hash
                ),

            "current_hash":
                str(
                    event.current_hash
                ),

            "payload":
                json.dumps(
                    event.payload,
                    default=str
                )

        }

    )