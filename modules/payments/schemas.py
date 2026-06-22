from pydantic import BaseModel

from typing import Optional


class CreatePaymentRequest(
    BaseModel
):

    merchant_id: str

    amount: float

    payment_method: str

    reference_type: str

    reference_id: str

    notes: Optional[str] = None