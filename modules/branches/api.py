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

from modules.branches.commands import (
    CreateBranchCommand,
    DeactivateBranchCommand,
    UpdateBranchCommand
)

from modules.branches.schemas import (
    CreateBranchRequest,
    DeactivateBranchRequest,
    UpdateBranchRequest
)

from modules.branches.query_service import (
    get_branch,
    get_branches,
    search_branches
)


router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
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
def create_branch_route(
    request: CreateBranchRequest,
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
            CreateBranchCommand(
                merchant_id=request.merchant_id,
                branch_id=request.branch_id,
                branch_code=request.branch_code,
                name=request.name,
                location=request.location,
                phone=request.phone,
                address=request.address,
                manager_user_id=request.manager_user_id,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.patch("/")
def update_branch_route(
    request: UpdateBranchRequest,
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
            UpdateBranchCommand(
                merchant_id=request.merchant_id,
                branch_id=request.branch_id,
                branch_code=request.branch_code,
                name=request.name,
                location=request.location,
                phone=request.phone,
                address=request.address,
                manager_user_id=request.manager_user_id,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/deactivate")
def deactivate_branch_route(
    request: DeactivateBranchRequest,
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
            DeactivateBranchCommand(
                merchant_id=request.merchant_id,
                branch_id=request.branch_id,
                reason=request.reason,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.get("/{merchant_id}")
def list_branches_route(
    merchant_id: str,
    include_inactive: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_branches(
        merchant_id=merchant_id,
        include_inactive=include_inactive
    )


@router.get("/{merchant_id}/search")
def search_branches_route(
    merchant_id: str,
    q: str = Query(min_length=1),
    include_inactive: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return search_branches(
        merchant_id=merchant_id,
        query_text=q,
        include_inactive=include_inactive
    )


@router.get("/{merchant_id}/{branch_id}")
def branch_detail_route(
    merchant_id: str,
    branch_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    branch = get_branch(
        merchant_id=merchant_id,
        branch_id=branch_id
    )

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found."
        )

    return branch