from dataclasses import dataclass


@dataclass
class Event:

    event_id: str

    event_type: str

    merchant_id: str

    timestamp: str

    previous_hash: str

    payload_hash: str

    event_hash: str

    payload: dict