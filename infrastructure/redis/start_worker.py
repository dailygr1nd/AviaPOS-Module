import threading

from infrastructure.projections.redis_worker import (
    start_projection_worker
)


def launch_workers():

    thread = threading.Thread(

        target=start_projection_worker,

        daemon=True

    )

    thread.start()