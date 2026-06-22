from infrastructure.redis.client import (
    redis_client
)


EVENT_STREAM = "aviapos_events"


def publish_event(event):

    redis_client.xadd(

        EVENT_STREAM,

        {

            "event_id":
                event.event_id,

            "event_type":
                event.event_type,

            "merchant_id":
                event.merchant_id,

            "aggregate_id":
                event.aggregate_id,

            "payload":
                str(event.payload)

        }

    )