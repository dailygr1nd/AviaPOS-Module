import json

from redis.exceptions import ResponseError

from infrastructure.redis.client import redis_client
from infrastructure.redis.streams import EVENT_STREAM

from modules.purchases.reactions import PurchaseReceivedReaction


PURCHASE_REACTION_GROUP_NAME = "purchase_reaction_workers"
PURCHASE_REACTION_CONSUMER_NAME = "purchase_reaction_worker_1"


def _ensure_group():
    try:
        redis_client.xgroup_create(
            EVENT_STREAM,
            PURCHASE_REACTION_GROUP_NAME,
            id="0",
            mkstream=True
        )

    except ResponseError as exc:
        if "BUSYGROUP" not in str(exc):
            raise


def _build_event(data: dict):
    class Event:
        pass

    event = Event()

    event.event_id = data.get("event_id")
    event.event_type = data.get("event_type")
    event.merchant_id = data.get("merchant_id")
    event.aggregate_id = data.get("aggregate_id")
    event.version = int(data.get("version", 1))
    event.payload = json.loads(
        data.get("payload", "{}")
    )

    return event


def start_purchase_reaction_worker():
    _ensure_group()

    reaction = PurchaseReceivedReaction()

    while True:
        messages = redis_client.xreadgroup(
            PURCHASE_REACTION_GROUP_NAME,
            PURCHASE_REACTION_CONSUMER_NAME,
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
                event = _build_event(data)

                try:
                    reaction.handle(event)

                    redis_client.xack(
                        EVENT_STREAM,
                        PURCHASE_REACTION_GROUP_NAME,
                        msg_id
                    )

                except Exception as exc:
                    print(
                        f"Purchase reaction failed for {event.event_id}: {exc}"
                    )