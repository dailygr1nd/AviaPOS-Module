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

from modules.inventory.commands import (
    AdjustInventoryCommand,
    DeductInventoryCommand,
    ReceiveInventoryCommand
)

from modules.inventory.schemas import (
    AdjustStockRequest,
    DeductStockRequest,
    ReceiveStockRequest
)

from modules.inventory.query_service import (
    get_branch_inventory,
    get_inventory,
    get_product_inventory
)


router = APIRouter(

    prefix="/inventory",

    tags=["Inventory"]

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


@router.post("/receive")
def receive_stock_route(

    request: ReceiveStockRequest,

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

            ReceiveInventoryCommand(

                merchant_id=
                    request.merchant_id,

                branch_id=
                    request.branch_id,

                product_id=
                    request.product_id,

                sku=
                    request.sku,

                quantity=
                    request.quantity,

                cost_price=
                    request.cost_price,

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


@router.post("/deduct")
def deduct_stock_route(

    request: DeductStockRequest,

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

            DeductInventoryCommand(

                merchant_id=
                    request.merchant_id,

                branch_id=
                    request.branch_id,

                product_id=
                    request.product_id,

                sku=
                    request.sku,

                quantity=
                    request.quantity,

                reason=
                    request.reason,

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


@router.post("/adjust")
def adjust_stock_route(

    request: AdjustStockRequest,

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

            AdjustInventoryCommand(

                merchant_id=
                    request.merchant_id,

                branch_id=
                    request.branch_id,

                product_id=
                    request.product_id,

                sku=
                    request.sku,

                adjustment=
                    request.adjustment,

                reason=
                    request.reason,

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
def list_inventory(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_inventory(
        merchant_id
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def branch_inventory(

    merchant_id: str,

    branch_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_branch_inventory(

        merchant_id,

        branch_id

    )


@router.get("/{merchant_id}/branch/{branch_id}/product/{product_id}")
def product_inventory(

    merchant_id: str,

    branch_id: str,

    product_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    item = get_product_inventory(

        merchant_id,

        branch_id,

        product_id

    )

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return item