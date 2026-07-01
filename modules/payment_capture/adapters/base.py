from dataclasses import dataclass
from typing import Optional


@dataclass
class NormalizedPaymentCapture:
    provider: str
    provider_channel: str
    provider_reference: str
    amount: float
    currency: str
    payment_method: str
    external_reference: Optional[str] = None
    payer_reference: Optional[str] = None
    payer_name: Optional[str] = None
    raw_payload: Optional[dict] = None


class PaymentCaptureAdapter:
    provider = "OTHER"

    def normalize(
        self,
        payload: dict
    ) -> NormalizedPaymentCapture:
        raise NotImplementedError