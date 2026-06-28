import threading

from infrastructure.outbox.worker import (
    start_outbox_worker
)


def launch_outbox_worker():

    thread = threading.Thread(

        target=start_outbox_worker,

        daemon=True

    )

    thread.start()