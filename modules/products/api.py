from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Query

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

from modules.products.commands import (
    CreateProductCommand,
    DeactivateProductCommand,
    UpdateProductCommand
)

from modules.products.schemas import (
    CreateProductRequest,
    DeactivateProductRequest,
    UpdateProductRequest
)

from modules.products.query_service import (
    get_product,
    get_product_by_sku,
    get_products,
    search_products
)


router = APIRouter(

    prefix="/products",

    tags=["Products"]

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
def create_product_route(

    request: CreateProductRequest,

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

            CreateProductCommand(

                merchant_id=
                    request.merchant_id,

                product_id=
                    request.product_id,

                sku=
                    request.sku,

                name=
                    request.name,

                selling_price=
                    request.selling_price,

                cost_price=
                    request.cost_price,

                category=
                    request.category,

                barcode=
                    request.barcode,

                idempotency_key=
                    idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.patch("/")
def update_product_route(

    request: UpdateProductRequest,

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

            UpdateProductCommand(

                merchant_id=
                    request.merchant_id,

                product_id=
                    request.product_id,

                sku=
                    request.sku,

                name=
                    request.name,

                selling_price=
                    request.selling_price,

                cost_price=
                    request.cost_price,

                category=
                    request.category,

                barcode=
                    request.barcode,

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


@router.post("/deactivate")
def deactivate_product_route(

    request: DeactivateProductRequest,

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

            DeactivateProductCommand(

                merchant_id=
                    request.merchant_id,

                product_id=
                    request.product_id,

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
def list_products_route(

    merchant_id: str,

    include_inactive: bool = Query(
        default=False
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_products(

        merchant_id=merchant_id,

        include_inactive=include_inactive

    )


@router.get("/{merchant_id}/search")
def search_products_route(

    merchant_id: str,

    q: str = Query(
        min_length=1
    ),

    include_inactive: bool = Query(
        default=False
    ),

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return search_products(

        merchant_id=merchant_id,

        query_text=q,

        include_inactive=include_inactive

    )


@router.get("/{merchant_id}/sku/{sku}")
def product_by_sku_route(

    merchant_id: str,

    sku: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    product = get_product_by_sku(

        merchant_id=merchant_id,

        sku=sku.strip().upper()

    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product


@router.get("/{merchant_id}/{product_id}")
def product_detail_route(

    merchant_id: str,

    product_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    product = get_product(

        merchant_id=merchant_id,

        product_id=product_id

    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product