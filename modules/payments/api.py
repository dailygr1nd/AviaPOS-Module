from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope
)

from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from infrastructure.concurrency.exceptions import (
    OptimisticConcurrencyError
)

from infrastructure.idempotency.repository import (
    IdempotencyConflict,
    IdempotencyInProgress
)

from modules.payments.commands import (
    CreatePaymentCommand,
    CompletePaymentCommand,
    FailPaymentCommand,
    CancelPaymentCommand
)

from modules.payments.schemas import (
    CreatePaymentRequest,
    CompletePaymentRequest,
    FailPaymentRequest,
    CancelPaymentRequest
)

from modules.payments.query_service import (
    get_payments
)


router = APIRouter(

    prefix="/payments",

    tags=["Payments"]

)


def _handle_command_error(
    exc: Exception
):

    if isinstance(
        exc,
        OptimisticConcurrencyError
    ):

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    if isinstance(
        exc,
        IdempotencyInProgress
    ):

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    if isinstance(
        exc,
        IdempotencyConflict
    ):

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    raise HTTPException(
        status_code=400,
        detail=str(exc)
    )


@router.post("/")
def create(

    request: CreatePaymentRequest,

    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    register_command_handlers()

    try:

        return command_bus.dispatch(

            CreatePaymentCommand(

                merchant_id=request.merchant_id,

                amount=request.amount,

                payment_method=request.payment_method,

                reference_type=request.reference_type,

                reference_id=request.reference_id,

                notes=request.notes,

                idempotency_key=idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.post("/complete")
def complete(

    request: CompletePaymentRequest,

    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),

    expected_version: int | None = Header(
        default=None,
        alias="X-Expected-Version"
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    if expected_version is None:

        raise HTTPException(
            status_code=428,
            detail="X-Expected-Version header is required."
        )

    register_command_handlers()

    try:

        return command_bus.dispatch(

            CompletePaymentCommand(

                merchant_id=request.merchant_id,

                payment_id=request.payment_id,

                expected_version=expected_version,

                idempotency_key=idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.post("/fail")
def fail(

    request: FailPaymentRequest,

    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),

    expected_version: int | None = Header(
        default=None,
        alias="X-Expected-Version"
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    if expected_version is None:

        raise HTTPException(
            status_code=428,
            detail="X-Expected-Version header is required."
        )

    register_command_handlers()

    try:

        return command_bus.dispatch(

            FailPaymentCommand(

                merchant_id=request.merchant_id,

                payment_id=request.payment_id,

                reason=request.reason,

                expected_version=expected_version,

                idempotency_key=idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.post("/cancel")
def cancel(

    request: CancelPaymentRequest,

    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),

    expected_version: int | None = Header(
        default=None,
        alias="X-Expected-Version"
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    if expected_version is None:

        raise HTTPException(
            status_code=428,
            detail="X-Expected-Version header is required."
        )

    register_command_handlers()

    try:

        return command_bus.dispatch(

            CancelPaymentCommand(

                merchant_id=request.merchant_id,

                payment_id=request.payment_id,

                reason=request.reason,

                expected_version=expected_version,

                idempotency_key=idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
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