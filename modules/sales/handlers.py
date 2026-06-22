from infrastructure.queue.jobs import (
    enqueue_projection_job
)


def sales_event_handler(

    event

):

    enqueue_projection_job(
        event
    )