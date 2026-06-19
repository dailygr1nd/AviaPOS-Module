from core.ledger.store import (
    load_events
)


def get_last_event_hash():

    events = load_events()

    if not events:

        return "GENESIS"

    return events[
        -1
    ][
        "event_hash"
    ]