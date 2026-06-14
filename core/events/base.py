from dataclasses import dataclass
from typing import Dict


@dataclass
class Event:

    event_id: str

    event_type: str

    merchant_id: str

    timestamp: str

    previous_hash: str

    payload_hash: str

    payload: Dict