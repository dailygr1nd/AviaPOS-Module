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

from modules.customers.commands import (
    CreateCustomerCommand,
    DeactivateCustomerCommand,
    UpdateCustomerCommand
)

from modules.customers.schemas import (
    CreateCustomerRequest,
    DeactivateCustomerRequest,
    UpdateCustomerRequest
)

from modules.customers.query_service import (
    get_customer,
    get_customers,
    search_customers
)


router = APIRouter(

    prefix="/customers",

    tags=["Customers"]

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
def create_customer_route(

    request: CreateCustomerRequest,

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

            CreateCustomerCommand(

                merchant_id=
                    request.merchant_id,

                customer_id=
                    request.customer_id,

                name=
                    request.name,

                phone=
                    request.phone,

                email=
                    str(request.email)
                    if request.email
                    else None,

                address=
                    request.address,

                customer_type=
                    request.customer_type,

                tax_id=
                    request.tax_id,

                credit_limit=
                    request.credit_limit,

                idempotency_key=
                    idempotency_key

            )

        )

    except Exception as exc:

        _handle_command_error(
            exc
        )


@router.patch("/")
def update_customer_route(

    request: UpdateCustomerRequest,

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

            UpdateCustomerCommand(

                merchant_id=
                    request.merchant_id,

                customer_id=
                    request.customer_id,

                name=
                    request.name,

                phone=
                    request.phone,

                email=
                    str(request.email)
                    if request.email
                    else None,

                address=
                    request.address,

                customer_type=
                    request.customer_type,

                tax_id=
                    request.tax_id,

                credit_limit=
                    request.credit_limit,

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
def deactivate_customer_route(

    request: DeactivateCustomerRequest,

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

            DeactivateCustomerCommand(

                merchant_id=
                    request.merchant_id,

                customer_id=
                    request.customer_id,

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
def list_customers_route(

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

    return get_customers(

        merchant_id=merchant_id,

        include_inactive=include_inactive

    )


@router.get("/{merchant_id}/search")
def search_customers_route(

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

    return search_customers(

        merchant_id=merchant_id,

        query_text=q,

        include_inactive=include_inactive

    )


@router.get("/{merchant_id}/{customer_id}")
def customer_detail_route(

    merchant_id: str,

    customer_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    customer = get_customer(

        merchant_id=merchant_id,

        customer_id=customer_id

    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer