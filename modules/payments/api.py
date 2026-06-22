from fastapi import APIRouter

from modules.payments.schemas import (
    CreatePaymentRequest
)

from modules.payments.service import (
    create_payment
)

from modules.payments.query_service import (
    get_payments
)


router = APIRouter(

    prefix="/payments",

    tags=["Payments"]

)


@router.post("/")
def create(

    request:
    CreatePaymentRequest

):

    return create_payment(

        merchant_id=
            request.merchant_id,

        amount=
            request.amount,

        payment_method=
            request.payment_method,

        reference_type=
            request.reference_type,

        reference_id=
            request.reference_id

    )


@router.get(
    "/{merchant_id}"
)
def payments(

    merchant_id: str

):

    return get_payments(
        merchant_id
    )