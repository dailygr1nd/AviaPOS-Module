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

from modules.transfers.commands import (
    CancelTransferCommand,
    ConfirmFundsMovementCommand,
    CreateFundsMovementIntentCommand,
    CreateStockTransferCommand,
    DispatchStockTransferCommand,
    DispatchStockTransferLineCommand,
    FailFundsMovementCommand,
    ReceiveStockTransferCommand,
    ReceiveStockTransferLineCommand,
    StockTransferLineCommand
)

from modules.transfers.query_service import (
    get_branch_transfers,
    get_transfer,
    get_transfers
)

from modules.transfers.schemas import (
    CancelTransferRequest,
    ConfirmFundsMovementRequest,
    CreateFundsMovementIntentRequest,
    CreateStockTransferRequest,
    DispatchStockTransferRequest,
    FailFundsMovementRequest,
    ReceiveStockTransferRequest
)


router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
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


@router.post("/stock")
def create_stock_transfer_route(
    request: CreateStockTransferRequest,
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
            CreateStockTransferCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                source_branch_id=request.source_branch_id,
                destination_branch_id=request.destination_branch_id,
                notes=request.notes,
                items=[
                    StockTransferLineCommand(
                        product_id=item.product_id,
                        sku=item.sku,
                        quantity=item.quantity
                    )
                    for item in request.items
                ],
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/stock/dispatch")
def dispatch_stock_transfer_route(
    request: DispatchStockTransferRequest,
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
            DispatchStockTransferCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                dispatched_by_user_id=request.dispatched_by_user_id,
                items=[
                    DispatchStockTransferLineCommand(
                        product_id=item.product_id,
                        sku=item.sku,
                        quantity=item.quantity,
                        source_inventory_expected_version=
                            item.source_inventory_expected_version
                    )
                    for item in request.items
                ],
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/stock/receive")
def receive_stock_transfer_route(
    request: ReceiveStockTransferRequest,
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
            ReceiveStockTransferCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                received_by_user_id=request.received_by_user_id,
                items=[
                    ReceiveStockTransferLineCommand(
                        product_id=item.product_id,
                        sku=item.sku,
                        quantity=item.quantity,
                        cost_price=item.cost_price,
                        destination_inventory_expected_version=
                            item.destination_inventory_expected_version
                    )
                    for item in request.items
                ],
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/funds-intent")
def create_funds_movement_intent_route(
    request: CreateFundsMovementIntentRequest,
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
            CreateFundsMovementIntentCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                source_branch_id=request.source_branch_id,
                destination_branch_id=request.destination_branch_id,
                amount=request.amount,
                currency=request.currency,
                destination_type=request.destination_type,
                destination_reference=request.destination_reference,
                purpose=request.purpose,
                rail_hint=request.rail_hint,
                external_reference=request.external_reference,
                railone_intent_id=request.railone_intent_id,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/funds/confirm")
def confirm_funds_movement_route(
    request: ConfirmFundsMovementRequest,
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
            ConfirmFundsMovementCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                provider_reference=request.provider_reference,
                external_reference=request.external_reference,
                railone_intent_id=request.railone_intent_id,
                reconciliation_state=request.reconciliation_state,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/funds/fail")
def fail_funds_movement_route(
    request: FailFundsMovementRequest,
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
            FailFundsMovementCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                reason=request.reason,
                provider_reference=request.provider_reference,
                external_reference=request.external_reference,
                railone_intent_id=request.railone_intent_id,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/cancel")
def cancel_transfer_route(
    request: CancelTransferRequest,
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
            CancelTransferCommand(
                merchant_id=request.merchant_id,
                transfer_id=request.transfer_id,
                reason=request.reason,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.get("/{merchant_id}")
def list_transfers_route(
    merchant_id: str,
    transfer_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_transfers(
        merchant_id=merchant_id,
        transfer_type=transfer_type,
        status=status
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def branch_transfers_route(
    merchant_id: str,
    branch_id: str,
    transfer_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_branch_transfers(
        merchant_id=merchant_id,
        branch_id=branch_id,
        transfer_type=transfer_type,
        status=status
    )


@router.get("/{merchant_id}/{transfer_id}")
def transfer_detail_route(
    merchant_id: str,
    transfer_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    transfer = get_transfer(
        merchant_id=merchant_id,
        transfer_id=transfer_id
    )

    if not transfer:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found."
        )

    return transfer