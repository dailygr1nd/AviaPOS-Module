from fastapi import APIRouter, Depends, Header, HTTPException, Query

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope
)

from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from infrastructure.concurrency.exceptions import OptimisticConcurrencyError

from infrastructure.idempotency.repository import (
    IdempotencyConflict,
    IdempotencyInProgress
)

from modules.purchases.commands import (
    CancelPurchaseCommand,
    CreatePurchaseCommand,
    PurchaseLineCommand,
    ReceivePurchaseCommand,
    ReceivePurchaseLineCommand
)

from modules.purchases.query_service import (
    get_branch_purchases,
    get_purchase,
    get_purchases,
    get_supplier_purchases
)

from modules.purchases.schemas import (
    CancelPurchaseRequest,
    CreatePurchaseRequest,
    ReceivePurchaseRequest
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


def _handle_command_error(exc: Exception):
    if isinstance(exc, OptimisticConcurrencyError):
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    if isinstance(exc, IdempotencyInProgress):
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    if isinstance(exc, IdempotencyConflict):
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    raise HTTPException(
        status_code=400,
        detail=str(exc)
    )


@router.post("/")
def create_purchase_route(
    request: CreatePurchaseRequest,
    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        request.merchant_id,
        current_user
    )

    register_command_handlers()

    try:
        return command_bus.dispatch(
            CreatePurchaseCommand(
                merchant_id=request.merchant_id,
                branch_id=request.branch_id,
                supplier_id=request.supplier_id,
                purchase_id=request.purchase_id,
                supplier_invoice_ref=request.supplier_invoice_ref,
                notes=request.notes,
                items=[
                    PurchaseLineCommand(
                        product_id=item.product_id,
                        sku=item.sku,
                        quantity=item.quantity,
                        unit_cost=item.unit_cost
                    )
                    for item in request.items
                ],
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/receive")
def receive_purchase_route(
    request: ReceivePurchaseRequest,
    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),
    expected_version: int | None = Header(
        default=None,
        alias="X-Expected-Version"
    ),
    current_user: AuthenticatedUser = Depends(get_current_user)
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
            ReceivePurchaseCommand(
                merchant_id=request.merchant_id,
                purchase_id=request.purchase_id,
                received_by_user_id=request.received_by_user_id,
                items=[
                    ReceivePurchaseLineCommand(
                        product_id=item.product_id,
                        sku=item.sku,
                        quantity=item.quantity,
                        cost_price=item.cost_price,
                        inventory_expected_version=item.inventory_expected_version
                    )
                    for item in request.items
                ],
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/cancel")
def cancel_purchase_route(
    request: CancelPurchaseRequest,
    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key"
    ),
    expected_version: int | None = Header(
        default=None,
        alias="X-Expected-Version"
    ),
    current_user: AuthenticatedUser = Depends(get_current_user)
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
            CancelPurchaseCommand(
                merchant_id=request.merchant_id,
                purchase_id=request.purchase_id,
                reason=request.reason,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.get("/{merchant_id}")
def list_purchases_route(
    merchant_id: str,
    status: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_purchases(
        merchant_id=merchant_id,
        status=status
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def branch_purchases_route(
    merchant_id: str,
    branch_id: str,
    status: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_branch_purchases(
        merchant_id=merchant_id,
        branch_id=branch_id,
        status=status
    )


@router.get("/{merchant_id}/supplier/{supplier_id}")
def supplier_purchases_route(
    merchant_id: str,
    supplier_id: str,
    status: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_supplier_purchases(
        merchant_id=merchant_id,
        supplier_id=supplier_id,
        status=status
    )


@router.get("/{merchant_id}/{purchase_id}")
def purchase_detail_route(
    merchant_id: str,
    purchase_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    purchase = get_purchase(
        merchant_id=merchant_id,
        purchase_id=purchase_id
    )

    if not purchase:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found."
        )

    return purchase