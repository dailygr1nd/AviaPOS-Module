from datetime import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class RegisterDeviceRequest(
    BaseModel
):

    merchant_id: str

    device_id: str

    branch_id: Optional[str] = None

    user_id: Optional[str] = None

    device_name: Optional[str] = None

    platform: str = "ANDROID"


class RegisterDeviceResponse(
    BaseModel
):

    success: bool

    merchant_id: str

    device_id: str

    status: str


class ClientSyncEvent(
    BaseModel
):

    client_event_id: str

    idempotency_key: str

    command_name: str

    payload: dict

    expected_version: Optional[int] = None

    occurred_at: Optional[datetime] = None


class PushSyncRequest(
    BaseModel
):

    merchant_id: str

    device_id: str

    branch_id: Optional[str] = None

    events: list[ClientSyncEvent] = Field(
        default_factory=list
    )


class PushSyncResponseItem(
    BaseModel
):

    client_event_id: str

    status: str

    server_sync_id: Optional[int] = None

    error: Optional[str] = None


class PullEventResponseItem(
    BaseModel
):

    id: int

    event_id: str

    event_type: str

    merchant_id: str

    aggregate_id: str

    version: int

    payload: dict

    previous_hash: str

    current_hash: str

    created_at: datetime


class SyncStatusResponse(
    BaseModel
):

    merchant_id: str

    device_id: str

    pending_count: int

    failed_count: int

    received_count: int