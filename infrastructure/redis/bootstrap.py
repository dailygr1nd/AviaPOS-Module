from infrastructure.redis.consumer import (
    create_group
)


def bootstrap_redis():

    create_group()