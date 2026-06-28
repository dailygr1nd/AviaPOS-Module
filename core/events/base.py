from dataclasses import dataclass
from dataclasses import field


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

    aggregate_id: str = "UNKNOWN"

    version: int = 1

    metadata: dict = field(
        default_factory=dict
    )

    @property
    def current_hash(self) -> str:

        return self.event_hash