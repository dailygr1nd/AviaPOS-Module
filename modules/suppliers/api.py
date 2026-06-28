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

from modules.suppliers.commands import (
    CreateSupplierCommand,
    DeactivateSupplierCommand,
    UpdateSupplierCommand
)

from modules.suppliers.schemas import (
    CreateSupplierRequest,
    DeactivateSupplierRequest,
    UpdateSupplierRequest
)

from modules.suppliers.query_service import (
    get_supplier,
    get_suppliers,
    search_suppliers
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
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
def create_supplier_route(
    request: CreateSupplierRequest,
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
            CreateSupplierCommand(
                merchant_id=request.merchant_id,
                supplier_id=request.supplier_id,
                supplier_code=request.supplier_code,
                name=request.name,
                contact_person=request.contact_person,
                phone=request.phone,
                email=str(request.email) if request.email else None,
                address=request.address,
                tax_id=request.tax_id,
                payment_terms=request.payment_terms,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.patch("/")
def update_supplier_route(
    request: UpdateSupplierRequest,
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
            UpdateSupplierCommand(
                merchant_id=request.merchant_id,
                supplier_id=request.supplier_id,
                supplier_code=request.supplier_code,
                name=request.name,
                contact_person=request.contact_person,
                phone=request.phone,
                email=str(request.email) if request.email else None,
                address=request.address,
                tax_id=request.tax_id,
                payment_terms=request.payment_terms,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/deactivate")
def deactivate_supplier_route(
    request: DeactivateSupplierRequest,
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
            DeactivateSupplierCommand(
                merchant_id=request.merchant_id,
                supplier_id=request.supplier_id,
                reason=request.reason,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.get("/{merchant_id}")
def list_suppliers_route(
    merchant_id: str,
    include_inactive: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_suppliers(
        merchant_id=merchant_id,
        include_inactive=include_inactive
    )


@router.get("/{merchant_id}/search")
def search_suppliers_route(
    merchant_id: str,
    q: str = Query(min_length=1),
    include_inactive: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return search_suppliers(
        merchant_id=merchant_id,
        query_text=q,
        include_inactive=include_inactive
    )


@router.get("/{merchant_id}/{supplier_id}")
def supplier_detail_route(
    merchant_id: str,
    supplier_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    supplier = get_supplier(
        merchant_id=merchant_id,
        supplier_id=supplier_id
    )

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    return supplier