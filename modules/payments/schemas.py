from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class CreatePaymentRequest(
    BaseModel
):

    merchant_id: str

    amount: float = Field(
        gt=0
    )

    payment_method: str

    reference_type: str

    reference_id: str

    notes: Optional[str] = None


class CompletePaymentRequest(
    BaseModel
):

    merchant_id: str

    payment_id: str


class FailPaymentRequest(
    BaseModel
):

    merchant_id: str

    payment_id: str

    reason: Optional[str] = None


class CancelPaymentRequest(
    BaseModel
):

    merchant_id: str

    payment_id: str

    reason: Optional[str] = None