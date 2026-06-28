from infrastructure.redis.client import (
    redis_client
)

from infrastructure.redis.streams import (
    EVENT_STREAM
)


GROUP_NAME = "projection_workers"

CONSUMER_NAME = "worker_1"

REACTION_GROUP_NAME = "sales_reaction_workers"

REACTION_CONSUMER_NAME = "sales_reaction_worker_1"


def _create_group(
    group_name: str
):

    try:

        redis_client.xgroup_create(

            EVENT_STREAM,

            group_name,

            id="0",

            mkstream=True

        )

    except Exception:

        pass


def create_group():

    _create_group(
        GROUP_NAME
    )


def create_projection_group():

    _create_group(
        GROUP_NAME
    )


def create_reaction_group():

    _create_group(
        REACTION_GROUP_NAME
    )


def create_groups():

    create_projection_group()

    create_reaction_group()