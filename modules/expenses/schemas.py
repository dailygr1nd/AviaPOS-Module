from pydantic import BaseModel

from typing import Optional


class ExpenseCreateRequest(
    BaseModel
):

    merchant_id: str

    branch_id: str

    category: str

    description: str

    amount: float

    reference: Optional[str] = None


class ExpenseApproveRequest(
    BaseModel
):

    merchant_id: str

    expense_id: str


class ExpensePayRequest(
    BaseModel
):

    merchant_id: str

    expense_id: str

    payment_method: str