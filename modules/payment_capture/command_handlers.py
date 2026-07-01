import uuid

from core.events.types import EventType
from core.ledger.event_factory import create_event

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.idempotency.request_hash import calculate_request_hash

from modules.branches.models import BranchProjection

from modules.payment_capture.commands import (
    CaptureExternalPaymentCommand,
    FailPaymentCaptureCommand,
    MatchPaymentCaptureCommand,
    ReconcilePaymentCaptureCommand
)

from modules.payment_capture.constants import (
    SUPPORTED_CAPTURE_CHANNELS,
    SUPPORTED_CAPTURE_PROVIDERS,
    SUPPORTED_RECONCILIATION_STATES,
    SUPPORTED_REFERENCE_TYPES
)

from modules.payment_capture.models import PaymentCaptureProjection


def _capture_aggregate_id(capture_id: str) -> str:
    return f"payment_capture:{capture_id}"


def _require_idempotency_key(idempotency_key: str | None):
    if not idempotency_key:
        raise ValueError(
            "Idempotency-Key header is required."
        )


def _normalize_optional_text(value: str | None):
    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    return value


def _normalize_upper(value: str | None):
    value = _normalize_optional_text(value)

    if value is None:
        return None

    return value.upper()


def _ensure_branch_exists(
    db,
    merchant_id: str,
    branch_id: str
):
    branch = (
        db.query(BranchProjection)
        .filter(
            BranchProjection.merchant_id == merchant_id,
            BranchProjection.branch_id == branch_id,
            BranchProjection.active == True
        )
        .first()
    )

    if not branch:
        raise ValueError(
            f"Active branch not found: {branch_id}"
        )


def _ensure_provider_reference_available(
    db,
    merchant_id: str,
    provider: str,
    provider_reference: str,
    capture_id: str | None = None
):
    query = (
        db.query(PaymentCaptureProjection)
        .filter(
            PaymentCaptureProjection.merchant_id == merchant_id,
            PaymentCaptureProjection.provider == provider,
            PaymentCaptureProjection.provider_reference
            == provider_reference
        )
    )

    if capture_id:
        query = query.filter(
            PaymentCaptureProjection.capture_id != capture_id
        )

    existing = query.first()

    if existing:
        raise ValueError(
            "Provider reference already captured for this merchant."
        )


def _get_capture_projection(
    db,
    merchant_id: str,
    capture_id: str
):
    return (
        db.query(PaymentCaptureProjection)
        .filter(
            PaymentCaptureProjection.merchant_id == merchant_id,
            PaymentCaptureProjection.capture_id == capture_id
        )
        .first()
    )


class CaptureExternalPaymentCommandHandler:
    def handle(self, command: CaptureExternalPaymentCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.amount <= 0:
            raise ValueError(
                "Captured amount must be greater than zero."
            )

        capture_id = command.capture_id or str(uuid.uuid4())

        provider = _normalize_upper(command.provider)

        if provider not in SUPPORTED_CAPTURE_PROVIDERS:
            raise ValueError(
                f"Unsupported capture provider: {command.provider}"
            )

        provider_channel = _normalize_upper(
            command.provider_channel
        )

        if provider_channel not in SUPPORTED_CAPTURE_CHANNELS:
            raise ValueError(
                f"Unsupported capture channel: {command.provider_channel}"
            )

        provider_reference = _normalize_optional_text(
            command.provider_reference
        )

        if not provider_reference:
            raise ValueError(
                "Provider reference is required."
            )

        currency = command.currency.strip().upper()

        if len(currency) != 3:
            raise ValueError(
                "Currency must be a 3-letter code."
            )

        payment_method = _normalize_upper(
            command.payment_method
        )

        reference_type = _normalize_upper(
            command.reference_type
        )

        if reference_type and reference_type not in SUPPORTED_REFERENCE_TYPES:
            raise ValueError(
                f"Unsupported reference_type: {command.reference_type}"
            )

        if reference_type and not command.reference_id:
            raise ValueError(
                "reference_id is required when reference_type is provided."
            )

        status = "MATCHED" if reference_type else "CAPTURED"
        reconciliation_state = "MATCHED" if reference_type else "PENDING"

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "capture_id": capture_id,
                "provider": provider,
                "provider_channel": provider_channel,
                "provider_reference": provider_reference,
                "external_reference": command.external_reference,
                "payer_reference": command.payer_reference,
                "payer_name": command.payer_name,
                "amount": command.amount,
                "currency": currency,
                "payment_method": payment_method,
                "reference_type": reference_type,
                "reference_id": command.reference_id,
                "railone_intent_id": command.railone_intent_id,
                "raw_payload": command.raw_payload or {}
            }
        )

        aggregate_id = _capture_aggregate_id(capture_id)

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CaptureExternalPaymentCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            if command.branch_id:
                _ensure_branch_exists(
                    uow.db,
                    command.merchant_id,
                    command.branch_id
                )

            _ensure_provider_reference_available(
                uow.db,
                command.merchant_id,
                provider,
                provider_reference
            )

            payload = {
                "capture_id": capture_id,
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "provider": provider,
                "provider_channel": provider_channel,
                "provider_reference": provider_reference,
                "external_reference": _normalize_optional_text(
                    command.external_reference
                ),
                "payer_reference": _normalize_optional_text(
                    command.payer_reference
                ),
                "payer_name": _normalize_optional_text(
                    command.payer_name
                ),
                "amount": command.amount,
                "currency": currency,
                "payment_method": payment_method,
                "reference_type": reference_type,
                "reference_id": _normalize_optional_text(
                    command.reference_id
                ),
                "railone_intent_id": _normalize_optional_text(
                    command.railone_intent_id
                ),
                "status": status,
                "reconciliation_state": reconciliation_state,
                "raw_payload": command.raw_payload or {},
                "metadata": {
                    "custody_model": "NON_CUSTODIAL",
                    "funds_held_by_avia": False
                }
            }

            event = create_event(
                EventType.PAYMENT_CAPTURE_RECEIVED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=1,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "custody_model": "NON_CUSTODIAL"
                }
            )

            persisted_event = uow.events.append(
                event,
                commit=False
            )

            uow.outbox.add_event(
                event,
                persisted_event_id=persisted_event.id
            )

            response = {
                "success": True,
                "capture_id": capture_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": status,
                "reconciliation_state": reconciliation_state,
                "custody_model": "NON_CUSTODIAL"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class MatchPaymentCaptureCommandHandler:
    def handle(self, command: MatchPaymentCaptureCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        reference_type = _normalize_upper(
            command.reference_type
        )

        if reference_type not in SUPPORTED_REFERENCE_TYPES:
            raise ValueError(
                f"Unsupported reference_type: {command.reference_type}"
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "capture_id": command.capture_id,
                "reference_type": reference_type,
                "reference_id": command.reference_id,
                "expected_version": command.expected_version,
                "notes": command.notes
            }
        )

        aggregate_id = _capture_aggregate_id(
            command.capture_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="MatchPaymentCaptureCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            capture = _get_capture_projection(
                uow.db,
                command.merchant_id,
                command.capture_id
            )

            if not capture:
                raise ValueError(
                    "Payment capture not found."
                )

            if capture.status not in {
                "CAPTURED",
                "MATCHED"
            }:
                raise ValueError(
                    f"Payment capture cannot be matched from status: {capture.status}"
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "capture_id": command.capture_id,
                "merchant_id": command.merchant_id,
                "reference_type": reference_type,
                "reference_id": command.reference_id,
                "notes": command.notes,
                "status": "MATCHED",
                "reconciliation_state": "MATCHED"
            }

            event = create_event(
                EventType.PAYMENT_CAPTURE_MATCHED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=next_version,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "expected_version": command.expected_version,
                    "custody_model": "NON_CUSTODIAL"
                }
            )

            persisted_event = uow.events.append(
                event,
                commit=False
            )

            uow.outbox.add_event(
                event,
                persisted_event_id=persisted_event.id
            )

            response = {
                "success": True,
                "capture_id": command.capture_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "MATCHED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class ReconcilePaymentCaptureCommandHandler:
    def handle(self, command: ReconcilePaymentCaptureCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        reconciliation_state = _normalize_upper(
            command.reconciliation_state
        )

        if reconciliation_state not in SUPPORTED_RECONCILIATION_STATES:
            raise ValueError(
                f"Unsupported reconciliation_state: {command.reconciliation_state}"
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "capture_id": command.capture_id,
                "expected_version": command.expected_version,
                "reconciliation_state": reconciliation_state,
                "provider_reference": command.provider_reference,
                "external_reference": command.external_reference,
                "railone_intent_id": command.railone_intent_id,
                "notes": command.notes
            }
        )

        aggregate_id = _capture_aggregate_id(
            command.capture_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="ReconcilePaymentCaptureCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            capture = _get_capture_projection(
                uow.db,
                command.merchant_id,
                command.capture_id
            )

            if not capture:
                raise ValueError(
                    "Payment capture not found."
                )

            if capture.status == "FAILED":
                raise ValueError(
                    "Failed payment capture cannot be reconciled."
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "capture_id": command.capture_id,
                "merchant_id": command.merchant_id,
                "reconciliation_state": reconciliation_state,
                "provider_reference": _normalize_optional_text(
                    command.provider_reference
                ),
                "external_reference": _normalize_optional_text(
                    command.external_reference
                ),
                "railone_intent_id": _normalize_optional_text(
                    command.railone_intent_id
                ),
                "notes": command.notes,
                "status": "RECONCILED"
            }

            event = create_event(
                EventType.PAYMENT_CAPTURE_RECONCILED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=next_version,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "expected_version": command.expected_version,
                    "custody_model": "NON_CUSTODIAL"
                }
            )

            persisted_event = uow.events.append(
                event,
                commit=False
            )

            uow.outbox.add_event(
                event,
                persisted_event_id=persisted_event.id
            )

            response = {
                "success": True,
                "capture_id": command.capture_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "RECONCILED",
                "reconciliation_state": reconciliation_state
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class FailPaymentCaptureCommandHandler:
    def handle(self, command: FailPaymentCaptureCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "capture_id": command.capture_id,
                "expected_version": command.expected_version,
                "reason": command.reason,
                "provider_reference": command.provider_reference,
                "external_reference": command.external_reference,
                "railone_intent_id": command.railone_intent_id
            }
        )

        aggregate_id = _capture_aggregate_id(
            command.capture_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="FailPaymentCaptureCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            capture = _get_capture_projection(
                uow.db,
                command.merchant_id,
                command.capture_id
            )

            if not capture:
                raise ValueError(
                    "Payment capture not found."
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "capture_id": command.capture_id,
                "merchant_id": command.merchant_id,
                "reason": command.reason,
                "provider_reference": _normalize_optional_text(
                    command.provider_reference
                ),
                "external_reference": _normalize_optional_text(
                    command.external_reference
                ),
                "railone_intent_id": _normalize_optional_text(
                    command.railone_intent_id
                ),
                "status": "FAILED",
                "reconciliation_state": "FAILED"
            }

            event = create_event(
                EventType.PAYMENT_CAPTURE_FAILED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=next_version,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "expected_version": command.expected_version,
                    "custody_model": "NON_CUSTODIAL"
                }
            )

            persisted_event = uow.events.append(
                event,
                commit=False
            )

            uow.outbox.add_event(
                event,
                persisted_event_id=persisted_event.id
            )

            response = {
                "success": True,
                "capture_id": command.capture_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "FAILED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response