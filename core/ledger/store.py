EVENT_STORE = []


def append_event(event):

    EVENT_STORE.append(event)


def get_events():

    return EVENT_STORE


def get_all_events():

    return EVENT_STORE


def load_events():

    return EVENT_STORE


def get_events_by_merchant(merchant_id: str):

    return [

        e for e in EVENT_STORE

        if e.get("merchant_id") == merchant_id

    ]