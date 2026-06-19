from core.ledger.store import get_events


def trace_by_field(field: str, value: str):

    events = get_events()

    results = []

    for event in events:

        payload = event.get("payload", {})

        if payload.get(field) == value:

            results.append(event)

    return results