from core.sync.sync_queue import (
    SyncQueue
)


class SyncWorker:

    def __init__(

        self,

        queue: SyncQueue

    ):

        self.queue = queue

    def run(

        self,

        merchant_id: str

    ):

        events = (

            self.queue.pending(

                merchant_id

            )

        )

        for event in events:

            print(

                f"SYNCING {event['event_id']}"

            )

            self.queue.mark_synced(

                event["event_id"]

            )