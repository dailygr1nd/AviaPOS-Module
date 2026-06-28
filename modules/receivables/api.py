from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope
)

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

    request: CreateReceivableRequest,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    try:

        return create_receivable(

            merchant_id=request.merchant_id,

            branch_id=request.branch_id,

            customer_id=request.customer_id,

            sale_id=request.sale_id,

            amount=request.amount

        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@router.post("/payment")
def payment(

    request: RecordPaymentRequest,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    try:

        return record_payment(

            receivable_id=request.receivable_id,

            merchant_id=request.merchant_id,

            amount=request.amount,

            payment_method=request.payment_method

        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@router.get("/summary/{merchant_id}")
def summary(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_receivables_summary(
        merchant_id
    )


@router.get("/{merchant_id}")
def list_receivables(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_open_receivables(
        merchant_id
    )