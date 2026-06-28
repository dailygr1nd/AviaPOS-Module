import time

from infrastructure.outbox.publisher import (
    OutboxPublisher
)


def start_outbox_worker(

    interval_seconds: int = 2

):

    publisher = OutboxPublisher()

    while True:

        try:

            publisher.publish_pending()

        except Exception as exc:

            print(
                f"Outbox worker error: {exc}"
            )

        time.sleep(
            interval_seconds
        )