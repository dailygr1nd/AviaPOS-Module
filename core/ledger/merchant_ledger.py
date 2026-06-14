from storage.sqlite.sqlite.event_store import (
    EventStore
)

from core.ledger.event_factory import (
    create_event
)


class MerchantLedger:

    def __init__(

        self,

        merchant_id,

        store: EventStore

    ):

        self.merchant_id = merchant_id

        self.store = store

    def latest_hash(self):

        events = self.store.all_events(
            self.merchant_id
        )

        if not events:

            return "GENESIS"

        return events[-1][
            "payload_hash"
        ]

    def append(

        self,

        event_type,

        payload

    ):

        event = create_event(

            event_type,

            self.merchant_id,

            payload,

            self.latest_hash()
        )

        self.store.append(
            event
        )

        return event