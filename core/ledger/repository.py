# core/ledger/repository.py

from core.ledger.store import (
    load_events
)


def get_all_events():

    return load_events()


def get_events_by_merchant(
    merchant_id: str
):

    return [

        event

        for event in load_events()

        if event["merchant_id"]
        == merchant_id

    ]


def get_events_by_type(
    event_type: str
):

    return [

        event

        for event in load_events()

        if event["event_type"]
        == event_type

    ]