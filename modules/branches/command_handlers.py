import uuid

from core.events.types import EventType
from core.ledger.event_factory import create_event

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.idempotency.request_hash import calculate_request_hash

from modules.branches.commands import (
    CreateBranchCommand,
    DeactivateBranchCommand,
    UpdateBranchCommand
)

from modules.branches.models import BranchProjection


def _branch_aggregate_id(branch_id: str) -> str:
    return f"branch:{branch_id}"


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


def _normalize_branch_code(value: str | None):
    value = _normalize_optional_text(value)

    if value is None:
        return None

    return value.upper()


def _ensure_branch_code_available(
    db,
    merchant_id: str,
    branch_code: str | None,
    branch_id: str | None = None
):
    if not branch_code:
        return

    query = (
        db.query(BranchProjection)
        .filter(
            BranchProjection.merchant_id == merchant_id,
            BranchProjection.branch_code == branch_code
        )
    )

    if branch_id:
        query = query.filter(
            BranchProjection.branch_id != branch_id
        )

    existing = query.first()

    if existing:
        raise ValueError(
            f"Branch code already exists for this merchant: {branch_code}"
        )


class CreateBranchCommandHandler:
    def handle(self, command: CreateBranchCommand):
        _require_idempotency_key(command.idempotency_key)

        if not command.name or not command.name.strip():
            raise ValueError("Branch name is required.")

        if not command.location or not command.location.strip():
            raise ValueError("Branch location is required.")

        branch_id = command.branch_id or str(uuid.uuid4())
        branch_code = _normalize_branch_code(command.branch_code)
        name = command.name.strip()
        location = command.location.strip()
        phone = _normalize_optional_text(command.phone)
        address = _normalize_optional_text(command.address)
        manager_user_id = _normalize_optional_text(command.manager_user_id)

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "branch_id": branch_id,
                "branch_code": branch_code,
                "name": name,
                "location": location,
                "phone": phone,
                "address": address,
                "manager_user_id": manager_user_id
            }
        )

        aggregate_id = _branch_aggregate_id(branch_id)

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CreateBranchCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_branch_code_available(
                uow.db,
                command.merchant_id,
                branch_code
            )

            payload = {
                "branch_id": branch_id,
                "merchant_id": command.merchant_id,
                "branch_code": branch_code,
                "name": name,
                "location": location,
                "phone": phone,
                "address": address,
                "manager_user_id": manager_user_id
            }

            event = create_event(
                EventType.BRANCH_CREATED,
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
                "branch_id": branch_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class UpdateBranchCommandHandler:
    def handle(self, command: UpdateBranchCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        changes = {}

        if command.branch_code is not None:
            changes["branch_code"] = _normalize_branch_code(
                command.branch_code
            )

        if command.name is not None:
            name = command.name.strip()

            if not name:
                raise ValueError(
                    "Branch name cannot be empty."
                )

            changes["name"] = name

        if command.location is not None:
            location = command.location.strip()

            if not location:
                raise ValueError(
                    "Branch location cannot be empty."
                )

            changes["location"] = location

        if command.phone is not None:
            changes["phone"] = _normalize_optional_text(
                command.phone
            )

        if command.address is not None:
            changes["address"] = _normalize_optional_text(
                command.address
            )

        if command.manager_user_id is not None:
            changes["manager_user_id"] = _normalize_optional_text(
                command.manager_user_id
            )

        if not changes:
            raise ValueError(
                "No branch changes provided."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "expected_version": command.expected_version,
                "changes": changes
            }
        )

        aggregate_id = _branch_aggregate_id(
            command.branch_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="UpdateBranchCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_branch_code_available(
                uow.db,
                command.merchant_id,
                changes.get("branch_code"),
                branch_id=command.branch_id
            )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "branch_id": command.branch_id,
                "merchant_id": command.merchant_id,
                **changes
            }

            event = create_event(
                EventType.BRANCH_UPDATED,
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
                "branch_id": command.branch_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class DeactivateBranchCommandHandler:
    def handle(self, command: DeactivateBranchCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "expected_version": command.expected_version,
                "reason": command.reason
            }
        )

        aggregate_id = _branch_aggregate_id(
            command.branch_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="DeactivateBranchCommand",
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
                "branch_id": command.branch_id,
                "merchant_id": command.merchant_id,
                "active": False,
                "reason": command.reason
            }

            event = create_event(
                EventType.BRANCH_UPDATED,
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
                "branch_id": command.branch_id,
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