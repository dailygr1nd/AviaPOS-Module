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

from modules.receivables.commands import (
    CreateReceivableCommand,
    RecordReceivablePaymentCommand
)

from modules.receivables.schemas import (
    CreateReceivableRequest,
    RecordPaymentRequest
)

from modules.receivables.query_service import (
    get_open_receivables,
    get_receivables_summary
)


router = APIRouter(

    prefix="/receivables",

    tags=["Receivables"]

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

    request: CreateReceivableRequest,

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

            CreateReceivableCommand(

                merchant_id=
                    request.merchant_id,

                branch_id=
                    request.branch_id,

                customer_id=
                    request.customer_id,

                sale_id=
                    request.sale_id,

                amount=
                    request.amount,

                idempotency_key=
                    idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.post("/payment")
def payment(

    request: RecordPaymentRequest,

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

            RecordReceivablePaymentCommand(

                merchant_id=
                    request.merchant_id,

                receivable_id=
                    request.receivable_id,

                amount=
                    request.amount,

                payment_method=
                    request.payment_method,

                expected_version=
                    expected_version,

                idempotency_key=
                    idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
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