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

from infrastructure.idempotency.repository import (
    IdempotencyConflict,
    IdempotencyInProgress
)

from modules.sales.commands import (
    CreateSaleCommand,
    SaleLineCommand
)

from modules.sales.schemas import (
    CreateSaleRequest,
    CreateSaleResponse
)

from modules.sales.query_service import (
    get_branch_sales,
    get_sale,
    get_sales,
    get_sales_summary
)


router = APIRouter(

    prefix="/sales",

    tags=["Sales"]

)


def _handle_command_error(
    exc: Exception
):

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


@router.post(
    "/",
    response_model=CreateSaleResponse
)
def create_sale_route(

    request: CreateSaleRequest,

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

        items = [

            SaleLineCommand(

                product_id=
                    item.product_id,

                sku=
                    item.sku,

                quantity=
                    item.quantity,

                unit_price=
                    item.unit_price,

                inventory_expected_version=
                    item.inventory_expected_version

            )

            for item in request.items

        ]

        return command_bus.dispatch(

            CreateSaleCommand(

                merchant_id=
                    request.merchant_id,

                branch_id=
                    request.branch_id,

                items=
                    items,

                payment_method=
                    request.payment_method,

                customer_id=
                    request.customer_id,

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

    return get_sales_summary(
        merchant_id
    )


@router.get("/{merchant_id}")
def list_sales(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_sales(
        merchant_id
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def list_branch_sales(

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

    return get_branch_sales(

        merchant_id,

        branch_id

    )


@router.get("/{merchant_id}/{sale_id}")
def sale_detail(

    merchant_id: str,

    sale_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    sale = get_sale(

        merchant_id,

        sale_id

    )

    if not sale:

        raise HTTPException(
            status_code=404,
            detail="Sale not found."
        )

    return sale