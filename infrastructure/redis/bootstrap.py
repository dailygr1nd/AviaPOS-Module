from infrastructure.redis.consumer import (
    create_groups
)


def bootstrap_redis():

    create_groups()