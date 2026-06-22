from pydantic import BaseModel


class CreateReceivableRequest(

    BaseModel

):

    merchant_id: str

    branch_id: str

    customer_id: str

    sale_id: str

    amount: float


class RecordPaymentRequest(

    BaseModel

):

    receivable_id: str

    merchant_id: str

    amount: float

    payment_method: str