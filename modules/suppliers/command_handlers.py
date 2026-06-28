import uuid

from core.events.types import EventType
from core.ledger.event_factory import create_event

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.idempotency.request_hash import calculate_request_hash

from modules.suppliers.commands import (
    CreateSupplierCommand,
    DeactivateSupplierCommand,
    UpdateSupplierCommand
)

from modules.suppliers.models import SupplierProjection


def _supplier_aggregate_id(supplier_id: str) -> str:
    return f"supplier:{supplier_id}"


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


def _normalize_email(value: str | None):
    value = _normalize_optional_text(value)

    if value is None:
        return None

    return value.lower()


def _normalize_supplier_code(value: str | None):
    value = _normalize_optional_text(value)

    if value is None:
        return None

    return value.upper()


def _ensure_unique_supplier_fields(
    db,
    merchant_id: str,
    supplier_code: str | None,
    phone: str | None,
    email: str | None,
    supplier_id: str | None = None
):
    checks = [
        ("supplier_code", supplier_code, SupplierProjection.supplier_code),
        ("phone", phone, SupplierProjection.phone),
        ("email", email, SupplierProjection.email)
    ]

    for label, value, column in checks:
        if not value:
            continue

        query = (
            db.query(SupplierProjection)
            .filter(
                SupplierProjection.merchant_id == merchant_id,
                column == value
            )
        )

        if supplier_id:
            query = query.filter(
                SupplierProjection.supplier_id != supplier_id
            )

        existing = query.first()

        if existing:
            raise ValueError(
                f"Supplier {label} already exists for this merchant: {value}"
            )


class CreateSupplierCommandHandler:
    def handle(self, command: CreateSupplierCommand):
        _require_idempotency_key(command.idempotency_key)

        if not command.name or not command.name.strip():
            raise ValueError("Supplier name is required.")

        supplier_id = command.supplier_id or str(uuid.uuid4())

        supplier_code = _normalize_supplier_code(command.supplier_code)
        name = command.name.strip()
        contact_person = _normalize_optional_text(command.contact_person)
        phone = _normalize_optional_text(command.phone)
        email = _normalize_email(command.email)
        address = _normalize_optional_text(command.address)
        tax_id = _normalize_optional_text(command.tax_id)
        payment_terms = _normalize_optional_text(command.payment_terms)

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "supplier_id": supplier_id,
                "supplier_code": supplier_code,
                "name": name,
                "contact_person": contact_person,
                "phone": phone,
                "email": email,
                "address": address,
                "tax_id": tax_id,
                "payment_terms": payment_terms
            }
        )

        aggregate_id = _supplier_aggregate_id(supplier_id)

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CreateSupplierCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_unique_supplier_fields(
                uow.db,
                command.merchant_id,
                supplier_code,
                phone,
                email
            )

            payload = {
                "supplier_id": supplier_id,
                "merchant_id": command.merchant_id,
                "supplier_code": supplier_code,
                "name": name,
                "contact_person": contact_person,
                "phone": phone,
                "email": email,
                "address": address,
                "tax_id": tax_id,
                "payment_terms": payment_terms
            }

            event = create_event(
                EventType.SUPPLIER_CREATED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=1,
                metadata={
                    "idempotency_key": command.idempotency_key
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
                "supplier_id": supplier_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class UpdateSupplierCommandHandler:
    def handle(self, command: UpdateSupplierCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        changes = {}

        if command.supplier_code is not None:
            changes["supplier_code"] = _normalize_supplier_code(
                command.supplier_code
            )

        if command.name is not None:
            name = command.name.strip()

            if not name:
                raise ValueError(
                    "Supplier name cannot be empty."
                )

            changes["name"] = name

        if command.contact_person is not None:
            changes["contact_person"] = _normalize_optional_text(
                command.contact_person
            )

        if command.phone is not None:
            changes["phone"] = _normalize_optional_text(command.phone)

        if command.email is not None:
            changes["email"] = _normalize_email(command.email)

        if command.address is not None:
            changes["address"] = _normalize_optional_text(command.address)

        if command.tax_id is not None:
            changes["tax_id"] = _normalize_optional_text(command.tax_id)

        if command.payment_terms is not None:
            changes["payment_terms"] = _normalize_optional_text(
                command.payment_terms
            )

        if not changes:
            raise ValueError(
                "No supplier changes provided."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "supplier_id": command.supplier_id,
                "expected_version": command.expected_version,
                "changes": changes
            }
        )

        aggregate_id = _supplier_aggregate_id(
            command.supplier_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="UpdateSupplierCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_unique_supplier_fields(
                uow.db,
                command.merchant_id,
                changes.get("supplier_code"),
                changes.get("phone"),
                changes.get("email"),
                supplier_id=command.supplier_id
            )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "supplier_id": command.supplier_id,
                "merchant_id": command.merchant_id,
                **changes
            }

            event = create_event(
                EventType.SUPPLIER_UPDATED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=next_version,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "expected_version": command.expected_version
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
                "supplier_id": command.supplier_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class DeactivateSupplierCommandHandler:
    def handle(self, command: DeactivateSupplierCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "supplier_id": command.supplier_id,
                "expected_version": command.expected_version,
                "reason": command.reason
            }
        )

        aggregate_id = _supplier_aggregate_id(
            command.supplier_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="DeactivateSupplierCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "supplier_id": command.supplier_id,
                "merchant_id": command.merchant_id,
                "active": False,
                "reason": command.reason
            }

            event = create_event(
                EventType.SUPPLIER_UPDATED,
                command.merchant_id,
                payload,
                previous_hash=uow.events.get_latest_hash(
                    command.merchant_id
                ),
                aggregate_id=aggregate_id,
                version=next_version,
                metadata={
                    "idempotency_key": command.idempotency_key,
                    "expected_version": command.expected_version
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
                "supplier_id": command.supplier_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "active": False
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response