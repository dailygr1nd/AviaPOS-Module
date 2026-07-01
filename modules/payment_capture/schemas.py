from typing import Optional

from pydantic import BaseModel, Field


class CaptureExternalPaymentRequest(BaseModel):
    merchant_id: str

    provider: str
    provider_channel: str
    provider_reference: str

    amount: float = Field(
        gt=0
    )

    currency: str = Field(
        min_length=3,
        max_length=3
    )

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


class MatchPaymentCaptureRequest(BaseModel):
    merchant_id: str
    capture_id: str
    reference_type: str
    reference_id: str
    notes: Optional[str] = None


class ReconcilePaymentCaptureRequest(BaseModel):
    merchant_id: str
    capture_id: str
    reconciliation_state: str = "RECONCILED"
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    notes: Optional[str] = None


class FailPaymentCaptureRequest(BaseModel):
    merchant_id: str
    capture_id: str
    reason: Optional[str] = None
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None