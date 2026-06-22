from infrastructure.queue.jobs import (
    enqueue_projection_job
)


def inventory_event_handler(

    event

):

    enqueue_projection_job(
        event
    )