from fastapi import APIRouter

from modules.expenses.schemas import (

    ExpenseCreateRequest,

    ExpenseApproveRequest,

    ExpensePayRequest

)

from modules.expenses.service import (

    create_expense,

    approve_expense,

    pay_expense

)

from modules.expenses.query_service import (

    get_expenses,

    get_expense_summary

)


router = APIRouter(

    prefix="/expenses",

    tags=["Expenses"]

)


@router.post("/")
def create(

    request:
    ExpenseCreateRequest

):

    return create_expense(

        merchant_id=
            request.merchant_id,

        branch_id=
            request.branch_id,

        category=
            request.category,

        description=
            request.description,

        amount=
            request.amount,

        reference=
            request.reference

    )


@router.get("/{merchant_id}")
def list_expenses(

    merchant_id: str

):

    return get_expenses(
        merchant_id
    )


@router.get(
    "/summary/{merchant_id}"
)
def summary(

    merchant_id: str

):

    return get_expense_summary(
        merchant_id
    )