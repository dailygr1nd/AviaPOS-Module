from dataclasses import dataclass

from typing import Optional


@dataclass
class SyncRecord:

    event_id: str

    merchant_id: str

    sync_status: str

    created_at: str

    updated_at: str


@dataclass
class ClientSyncEnvelope:

    merchant_id: str

    device_id: str

    client_event_id: str

    idempotency_key: str

    command_name: str

    payload: dict

    branch_id: Optional[str] = None

    expected_version: Optional[int] = None

    occurred_at: Optional[str] = None