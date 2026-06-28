from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException

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

from modules.expenses.commands import (
    CreateExpenseCommand,
    ApproveExpenseCommand,
    PayExpenseCommand
)

from modules.expenses.schemas import (
    ExpenseCreateRequest,
    ExpenseApproveRequest,
    ExpensePayRequest
)

from modules.expenses.query_service import (
    get_expenses,
    get_expense_summary
)


router = APIRouter(

    prefix="/expenses",

    tags=["Expenses"]

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

            detail=str(
                exc
            )

        )

    if isinstance(
        exc,
        IdempotencyInProgress
    ):

        raise HTTPException(

            status_code=409,

            detail=str(
                exc
            )

        )

    if isinstance(
        exc,
        IdempotencyConflict
    ):

        raise HTTPException(

            status_code=409,

            detail=str(
                exc
            )

        )

    raise HTTPException(

        status_code=400,

        detail=str(
            exc
        )

    )


@router.post("/")
def create(

    request: ExpenseCreateRequest,

    idempotency_key: str | None = Header(

        default=None,

        alias="Idempotency-Key"

    )

):

    register_command_handlers()

    try:

        return command_bus.dispatch(

            CreateExpenseCommand(

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
                    request.reference,

                idempotency_key=
                    idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.post("/approve")
def approve(

    request: ExpenseApproveRequest,

    idempotency_key: str | None = Header(

        default=None,

        alias="Idempotency-Key"

    ),

    expected_version: int | None = Header(

        default=None,

        alias="X-Expected-Version"

    )

):

    register_command_handlers()

    if expected_version is None:

        raise HTTPException(

            status_code=428,

            detail="X-Expected-Version header is required."

        )

    try:

        return command_bus.dispatch(

            ApproveExpenseCommand(

                merchant_id=
                    request.merchant_id,

                expense_id=
                    request.expense_id,

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


@router.post("/pay")
def pay(

    request: ExpensePayRequest,

    idempotency_key: str | None = Header(

        default=None,

        alias="Idempotency-Key"

    ),

    expected_version: int | None = Header(

        default=None,

        alias="X-Expected-Version"

    )

):

    register_command_handlers()

    if expected_version is None:

        raise HTTPException(

            status_code=428,

            detail="X-Expected-Version header is required."

        )

    try:

        return command_bus.dispatch(

            PayExpenseCommand(

                merchant_id=
                    request.merchant_id,

                expense_id=
                    request.expense_id,

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


@router.get("/{merchant_id}")
def list_expenses(
    merchant_id: str
):

    return get_expenses(
        merchant_id
    )


@router.get("/summary/{merchant_id}")
def summary(
    merchant_id: str
):

    return get_expense_summary(
        merchant_id
    )