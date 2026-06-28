from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope
)

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

    request: CreatePaymentRequest,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    try:

        return create_payment(

            merchant_id=request.merchant_id,

            amount=request.amount,

            payment_method=request.payment_method,

            reference_type=request.reference_type,

            reference_id=request.reference_id

        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@router.get("/{merchant_id}")
def payments(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_payments(
        merchant_id
    )