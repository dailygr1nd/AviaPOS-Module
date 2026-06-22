from infrastructure.redis.client import (
    redis_client
)

from infrastructure.redis.streams import (
    EVENT_STREAM
)


GROUP_NAME = "projection_workers"

CONSUMER_NAME = "worker_1"


def create_group():

    try:

        redis_client.xgroup_create(

            EVENT_STREAM,

            GROUP_NAME,

            id="0",

            mkstream=True

        )

    except Exception:

        pass