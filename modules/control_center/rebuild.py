from core.ledger.store import get_all_events

from core.projections.bootstrap import engine


def rebuild():

    engine.rebuild()

    return {
        "status": "rebuilt",
        "events_replayed": len(get_all_events())
    }