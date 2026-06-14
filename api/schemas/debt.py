from pydantic import (
    BaseModel,
    Field
)

class CreateDebtRequest(

    BaseModel

):

    merchant_id: str

    customer_id: str

    amount: float = Field(
        gt=0
    )

    currency: str

    due_date: str

class SettleDebtRequest(

    BaseModel

):

    merchant_id: str

    debt_id: str

    customer_id: str

    amount: float = Field(
        gt=0
    )

    currency: str