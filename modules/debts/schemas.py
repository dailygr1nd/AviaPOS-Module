from pydantic import BaseModel


class CreateDebtRequest(BaseModel):

    merchant_id: str
    debt_id: str
    customer_id: str
    sale_id: str
    amount: float


class RecordPaymentRequest(BaseModel):

    merchant_id: str
    debt_id: str
    amount: float
    method: str