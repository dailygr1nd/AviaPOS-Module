from fastapi import APIRouter

from modules.receivables.schemas import (

    CreateReceivableRequest,

    RecordPaymentRequest

)

from modules.receivables.service import (

    create_receivable,

    record_payment

)

from modules.receivables.query_service import (

    get_open_receivables,

    get_receivables_summary

)


router = APIRouter(

    prefix="/receivables",

    tags=["Receivables"]

)


@router.post("/")
def create(

    request:
    CreateReceivableRequest

):

    return create_receivable(

        merchant_id=
            request.merchant_id,

        branch_id=
            request.branch_id,

        customer_id=
            request.customer_id,

        sale_id=
            request.sale_id,

        amount=
            request.amount

    )


@router.post(
    "/payment"
)
def payment(

    request:
    RecordPaymentRequest

):

    return record_payment(

        receivable_id=
            request.receivable_id,

        merchant_id=
            request.merchant_id,

        amount=
            request.amount,

        payment_method=
            request.payment_method

    )


@router.get(
    "/{merchant_id}"
)
def list_receivables(

    merchant_id: str

):

    return get_open_receivables(
        merchant_id
    )


@router.get(
    "/summary/{merchant_id}"
)
def summary(

    merchant_id: str

):

    return get_receivables_summary(
        merchant_id
    )