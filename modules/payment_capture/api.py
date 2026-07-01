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

from modules.payment_capture.commands import (
    CaptureExternalPaymentCommand,
    FailPaymentCaptureCommand,
    MatchPaymentCaptureCommand,
    ReconcilePaymentCaptureCommand
)

from modules.payment_capture.query_service import (
    get_branch_payment_captures,
    get_payment_capture,
    get_payment_captures,
    search_payment_captures
)

from modules.payment_capture.schemas import (
    CaptureExternalPaymentRequest,
    FailPaymentCaptureRequest,
    MatchPaymentCaptureRequest,
    ReconcilePaymentCaptureRequest
)


router = APIRouter(
    prefix="/payment-captures",
    tags=["Payment Capture"]
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
def capture_external_payment_route(
    request: CaptureExternalPaymentRequest,
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
            CaptureExternalPaymentCommand(
                merchant_id=request.merchant_id,
                branch_id=request.branch_id,
                capture_id=request.capture_id,
                provider=request.provider,
                provider_channel=request.provider_channel,
                provider_reference=request.provider_reference,
                external_reference=request.external_reference,
                payer_reference=request.payer_reference,
                payer_name=request.payer_name,
                amount=request.amount,
                currency=request.currency,
                payment_method=request.payment_method,
                reference_type=request.reference_type,
                reference_id=request.reference_id,
                railone_intent_id=request.railone_intent_id,
                raw_payload=request.raw_payload,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/match")
def match_payment_capture_route(
    request: MatchPaymentCaptureRequest,
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
            MatchPaymentCaptureCommand(
                merchant_id=request.merchant_id,
                capture_id=request.capture_id,
                reference_type=request.reference_type,
                reference_id=request.reference_id,
                notes=request.notes,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/reconcile")
def reconcile_payment_capture_route(
    request: ReconcilePaymentCaptureRequest,
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
            ReconcilePaymentCaptureCommand(
                merchant_id=request.merchant_id,
                capture_id=request.capture_id,
                reconciliation_state=request.reconciliation_state,
                provider_reference=request.provider_reference,
                external_reference=request.external_reference,
                railone_intent_id=request.railone_intent_id,
                notes=request.notes,
                expected_version=expected_version,
                idempotency_key=idempotency_key
            )
        )

    except Exception as exc:
        _handle_command_error(exc)


@router.post("/fail")
def fail_payment_capture_route(
    request: FailPaymentCaptureRequest,
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
            FailPaymentCaptureCommand(
                merchant_id=request.merchant_id,
                capture_id=request.capture_id,
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


@router.get("/{merchant_id}")
def list_payment_captures_route(
    merchant_id: str,
    status: str | None = Query(default=None),
    provider: str | None = Query(default=None),
    reference_type: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_payment_captures(
        merchant_id=merchant_id,
        status=status,
        provider=provider,
        reference_type=reference_type
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def branch_payment_captures_route(
    merchant_id: str,
    branch_id: str,
    status: str | None = Query(default=None),
    provider: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_branch_payment_captures(
        merchant_id=merchant_id,
        branch_id=branch_id,
        status=status,
        provider=provider
    )


@router.get("/{merchant_id}/search")
def search_payment_captures_route(
    merchant_id: str,
    q: str = Query(min_length=1),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    return search_payment_captures(
        merchant_id=merchant_id,
        query_text=q
    )


@router.get("/{merchant_id}/{capture_id}")
def payment_capture_detail_route(
    merchant_id: str,
    capture_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    require_merchant_scope(
        merchant_id,
        current_user
    )

    capture = get_payment_capture(
        merchant_id=merchant_id,
        capture_id=capture_id
    )

    if not capture:
        raise HTTPException(
            status_code=404,
            detail="Payment capture not found."
        )

    return capture