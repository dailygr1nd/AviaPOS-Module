from dataclasses import dataclass
from typing import Optional

from core.commands.command import Command


@dataclass
class CaptureExternalPaymentCommand(Command):
    merchant_id: str
    provider: str
    provider_channel: str
    provider_reference: str
    amount: float
    currency: str
    payment_method: str
    branch_id: Optional[str] = None
    capture_id: Optional[str] = None
    external_reference: Optional[str] = None
    payer_reference: Optional[str] = None
    payer_name: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    railone_intent_id: Optional[str] = None
    raw_payload: Optional[dict] = None
    idempotency_key: Optional[str] = None


@dataclass
class MatchPaymentCaptureCommand(Command):
    merchant_id: str
    capture_id: str
    reference_type: str
    reference_id: str
    expected_version: int
    notes: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class ReconcilePaymentCaptureCommand(Command):
    merchant_id: str
    capture_id: str
    expected_version: int
    reconciliation_state: str = "RECONCILED"
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    notes: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class FailPaymentCaptureCommand(Command):
    merchant_id: str
    capture_id: str
    expected_version: int
    reason: Optional[str] = None
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    idempotency_key: Optional[str] = None