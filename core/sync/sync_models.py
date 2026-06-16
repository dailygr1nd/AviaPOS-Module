from dataclasses import dataclass


@dataclass
class SyncRecord:

    event_id: str

    merchant_id: str

    sync_status: str

    created_at: str

    updated_at: str