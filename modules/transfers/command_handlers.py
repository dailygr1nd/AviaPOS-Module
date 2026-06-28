import uuid

from core.events.types import EventType
from core.ledger.event_factory import create_event

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.idempotency.request_hash import calculate_request_hash

from modules.branches.models import BranchProjection
from modules.products.models import ProductProjection
from modules.suppliers.models import SupplierProjection

from modules.transfers.commands import (
    CancelTransferCommand,
    ConfirmFundsMovementCommand,
    CreateFundsMovementIntentCommand,
    CreateStockTransferCommand,
    DispatchStockTransferCommand,
    FailFundsMovementCommand,
    ReceiveStockTransferCommand
)

from modules.transfers.models import TransferProjection


VALID_DESTINATION_TYPES = {
    "BRANCH",
    "SUPPLIER",
    "BANK_ACCOUNT",
    "MOBILE_MONEY_TILL",
    "MOBILE_MONEY_PAYBILL",
    "EXTERNAL_MERCHANT",
    "RAILONE_ALIAS"
}


def _transfer_aggregate_id(transfer_id: str) -> str:
    return f"transfer:{transfer_id}"


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


def _normalize_sku(value: str) -> str:
    return value.strip().upper()


def _ensure_branch_exists(db, merchant_id: str, branch_id: str):
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


def _ensure_product_exists(db, merchant_id: str, product_id: str):
    product = (
        db.query(ProductProjection)
        .filter(
            ProductProjection.merchant_id == merchant_id,
            ProductProjection.product_id == product_id,
            ProductProjection.active == True
        )
        .first()
    )

    if not product:
        raise ValueError(
            f"Active product not found: {product_id}"
        )


def _ensure_supplier_exists(db, merchant_id: str, supplier_id: str):
    supplier = (
        db.query(SupplierProjection)
        .filter(
            SupplierProjection.merchant_id == merchant_id,
            SupplierProjection.supplier_id == supplier_id,
            SupplierProjection.active == True
        )
        .first()
    )

    if not supplier:
        raise ValueError(
            f"Active supplier not found: {supplier_id}"
        )


def _get_transfer_projection(
    db,
    merchant_id: str,
    transfer_id: str
):
    return (
        db.query(TransferProjection)
        .filter(
            TransferProjection.merchant_id == merchant_id,
            TransferProjection.transfer_id == transfer_id
        )
        .first()
    )


def _normalize_stock_items(
    db,
    merchant_id: str,
    items
):
    if not items:
        raise ValueError(
            "Transfer must contain at least one item."
        )

    normalized = []

    for item in items:
        if item.quantity <= 0:
            raise ValueError(
                "Transfer item quantity must be greater than zero."
            )

        _ensure_product_exists(
            db,
            merchant_id,
            item.product_id
        )

        normalized.append(
            {
                "product_id": item.product_id,
                "sku": _normalize_sku(item.sku),
                "quantity": item.quantity
            }
        )

    return normalized


def _normalize_dispatch_items(
    db,
    merchant_id: str,
    items
):
    if not items:
        raise ValueError(
            "Dispatch must contain at least one item."
        )

    normalized = []

    for item in items:
        if item.quantity <= 0:
            raise ValueError(
                "Dispatch item quantity must be greater than zero."
            )

        if item.source_inventory_expected_version < 0:
            raise ValueError(
                "source_inventory_expected_version cannot be negative."
            )

        _ensure_product_exists(
            db,
            merchant_id,
            item.product_id
        )

        normalized.append(
            {
                "product_id": item.product_id,
                "sku": _normalize_sku(item.sku),
                "quantity": item.quantity,
                "source_inventory_expected_version":
                    item.source_inventory_expected_version
            }
        )

    return normalized


def _normalize_receive_items(
    db,
    merchant_id: str,
    items
):
    if not items:
        raise ValueError(
            "Receipt must contain at least one item."
        )

    normalized = []

    for item in items:
        if item.quantity <= 0:
            raise ValueError(
                "Receipt item quantity must be greater than zero."
            )

        if item.cost_price < 0:
            raise ValueError(
                "Receipt item cost_price cannot be negative."
            )

        if item.destination_inventory_expected_version < 0:
            raise ValueError(
                "destination_inventory_expected_version cannot be negative."
            )

        _ensure_product_exists(
            db,
            merchant_id,
            item.product_id
        )

        normalized.append(
            {
                "product_id": item.product_id,
                "sku": _normalize_sku(item.sku),
                "quantity": item.quantity,
                "cost_price": item.cost_price,
                "destination_inventory_expected_version":
                    item.destination_inventory_expected_version
            }
        )

    return normalized


def _normalize_destination_type(value: str) -> str:
    normalized = value.strip().upper()

    if normalized not in VALID_DESTINATION_TYPES:
        raise ValueError(
            f"Unsupported destination_type: {value}"
        )

    return normalized


class CreateStockTransferCommandHandler:
    def handle(self, command: CreateStockTransferCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.source_branch_id == command.destination_branch_id:
            raise ValueError(
                "Source and destination branches cannot be the same."
            )

        transfer_id = command.transfer_id or str(uuid.uuid4())

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": transfer_id,
                "source_branch_id": command.source_branch_id,
                "destination_branch_id": command.destination_branch_id,
                "notes": command.notes,
                "items": [
                    item.__dict__
                    for item in command.items
                ]
            }
        )

        aggregate_id = _transfer_aggregate_id(
            transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CreateStockTransferCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_branch_exists(
                uow.db,
                command.merchant_id,
                command.source_branch_id
            )

            _ensure_branch_exists(
                uow.db,
                command.merchant_id,
                command.destination_branch_id
            )

            normalized_items = _normalize_stock_items(
                uow.db,
                command.merchant_id,
                command.items
            )

            payload = {
                "transfer_id": transfer_id,
                "merchant_id": command.merchant_id,
                "transfer_type": "STOCK_TRANSFER",
                "source_branch_id": command.source_branch_id,
                "destination_branch_id": command.destination_branch_id,
                "notes": command.notes,
                "items": normalized_items,
                "status": "STOCK_CREATED"
            }

            event = create_event(
                EventType.TRANSFER_CREATED,
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
                "transfer_id": transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "STOCK_CREATED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class DispatchStockTransferCommandHandler:
    def handle(self, command: DispatchStockTransferCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": command.transfer_id,
                "expected_version": command.expected_version,
                "dispatched_by_user_id": command.dispatched_by_user_id,
                "items": [
                    item.__dict__
                    for item in command.items
                ]
            }
        )

        aggregate_id = _transfer_aggregate_id(
            command.transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="DispatchStockTransferCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            transfer = _get_transfer_projection(
                uow.db,
                command.merchant_id,
                command.transfer_id
            )

            if not transfer:
                raise ValueError(
                    "Transfer not found."
                )

            if transfer.transfer_type != "STOCK_TRANSFER":
                raise ValueError(
                    "Only stock transfers can be dispatched."
                )

            if transfer.status != "STOCK_CREATED":
                raise ValueError(
                    f"Transfer cannot be dispatched from status: {transfer.status}"
                )

            normalized_items = _normalize_dispatch_items(
                uow.db,
                command.merchant_id,
                command.items
            )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "transfer_id": command.transfer_id,
                "merchant_id": command.merchant_id,
                "transfer_type": "STOCK_TRANSFER",
                "source_branch_id": transfer.source_branch_id,
                "destination_branch_id": transfer.destination_branch_id,
                "items": normalized_items,
                "dispatched_by_user_id": command.dispatched_by_user_id,
                "status": "STOCK_DISPATCHED"
            }

            event = create_event(
                EventType.TRANSFER_DISPATCHED,
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
                "transfer_id": command.transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "STOCK_DISPATCHED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class ReceiveStockTransferCommandHandler:
    def handle(self, command: ReceiveStockTransferCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": command.transfer_id,
                "expected_version": command.expected_version,
                "received_by_user_id": command.received_by_user_id,
                "items": [
                    item.__dict__
                    for item in command.items
                ]
            }
        )

        aggregate_id = _transfer_aggregate_id(
            command.transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="ReceiveStockTransferCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            transfer = _get_transfer_projection(
                uow.db,
                command.merchant_id,
                command.transfer_id
            )

            if not transfer:
                raise ValueError(
                    "Transfer not found."
                )

            if transfer.transfer_type != "STOCK_TRANSFER":
                raise ValueError(
                    "Only stock transfers can be received."
                )

            if transfer.status != "STOCK_DISPATCHED":
                raise ValueError(
                    f"Transfer cannot be received from status: {transfer.status}"
                )

            normalized_items = _normalize_receive_items(
                uow.db,
                command.merchant_id,
                command.items
            )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "transfer_id": command.transfer_id,
                "merchant_id": command.merchant_id,
                "transfer_type": "STOCK_TRANSFER",
                "source_branch_id": transfer.source_branch_id,
                "destination_branch_id": transfer.destination_branch_id,
                "items": normalized_items,
                "received_by_user_id": command.received_by_user_id,
                "status": "STOCK_RECEIVED"
            }

            event = create_event(
                EventType.TRANSFER_RECEIVED,
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
                "transfer_id": command.transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "STOCK_RECEIVED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class CancelTransferCommandHandler:
    def handle(self, command: CancelTransferCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": command.transfer_id,
                "expected_version": command.expected_version,
                "reason": command.reason
            }
        )

        aggregate_id = _transfer_aggregate_id(
            command.transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CancelTransferCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            transfer = _get_transfer_projection(
                uow.db,
                command.merchant_id,
                command.transfer_id
            )

            if not transfer:
                raise ValueError(
                    "Transfer not found."
                )

            if transfer.status not in {
                "STOCK_CREATED",
                "FUNDS_INTENT_CREATED"
            }:
                raise ValueError(
                    f"Transfer cannot be cancelled from status: {transfer.status}"
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "transfer_id": command.transfer_id,
                "merchant_id": command.merchant_id,
                "transfer_type": transfer.transfer_type,
                "reason": command.reason,
                "status": "CANCELLED"
            }

            event = create_event(
                EventType.TRANSFER_CANCELLED,
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
                "transfer_id": command.transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "CANCELLED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class CreateFundsMovementIntentCommandHandler:
    def handle(self, command: CreateFundsMovementIntentCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.amount <= 0:
            raise ValueError(
                "Amount must be greater than zero."
            )

        transfer_id = command.transfer_id or str(uuid.uuid4())

        currency = command.currency.strip().upper()

        if len(currency) != 3:
            raise ValueError(
                "Currency must be a 3-letter code."
            )

        destination_type = _normalize_destination_type(
            command.destination_type
        )

        destination_reference = _normalize_optional_text(
            command.destination_reference
        )

        if not destination_reference:
            raise ValueError(
                "Destination reference is required."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": transfer_id,
                "source_branch_id": command.source_branch_id,
                "destination_branch_id": command.destination_branch_id,
                "amount": command.amount,
                "currency": currency,
                "destination_type": destination_type,
                "destination_reference": destination_reference,
                "purpose": command.purpose,
                "rail_hint": command.rail_hint,
                "external_reference": command.external_reference,
                "railone_intent_id": command.railone_intent_id
            }
        )

        aggregate_id = _transfer_aggregate_id(
            transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CreateFundsMovementIntentCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            if command.source_branch_id:
                _ensure_branch_exists(
                    uow.db,
                    command.merchant_id,
                    command.source_branch_id
                )

            if destination_type == "BRANCH":
                if not command.destination_branch_id:
                    raise ValueError(
                        "destination_branch_id is required for BRANCH destination."
                    )

                _ensure_branch_exists(
                    uow.db,
                    command.merchant_id,
                    command.destination_branch_id
                )

            if destination_type == "SUPPLIER":
                _ensure_supplier_exists(
                    uow.db,
                    command.merchant_id,
                    destination_reference
                )

            payload = {
                "transfer_id": transfer_id,
                "merchant_id": command.merchant_id,
                "transfer_type": "FUNDS_MOVEMENT_INTENT",
                "source_branch_id": command.source_branch_id,
                "destination_branch_id": command.destination_branch_id,
                "destination_type": destination_type,
                "destination_reference": destination_reference,
                "amount": command.amount,
                "currency": currency,
                "purpose": _normalize_optional_text(command.purpose),
                "rail_hint": _normalize_optional_text(command.rail_hint),
                "external_reference":
                    _normalize_optional_text(command.external_reference),
                "railone_intent_id":
                    _normalize_optional_text(command.railone_intent_id),
                "status": "FUNDS_INTENT_CREATED",
                "metadata": {
                    "custody_model": "NON_CUSTODIAL",
                    "funds_held_by_avia": False
                }
            }

            event = create_event(
                EventType.TRANSFER_FUNDS_INTENT_CREATED,
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
                "transfer_id": transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "FUNDS_INTENT_CREATED",
                "custody_model": "NON_CUSTODIAL"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class ConfirmFundsMovementCommandHandler:
    def handle(self, command: ConfirmFundsMovementCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": command.transfer_id,
                "expected_version": command.expected_version,
                "provider_reference": command.provider_reference,
                "external_reference": command.external_reference,
                "railone_intent_id": command.railone_intent_id,
                "reconciliation_state": command.reconciliation_state
            }
        )

        aggregate_id = _transfer_aggregate_id(
            command.transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="ConfirmFundsMovementCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            transfer = _get_transfer_projection(
                uow.db,
                command.merchant_id,
                command.transfer_id
            )

            if not transfer:
                raise ValueError(
                    "Transfer not found."
                )

            if transfer.transfer_type != "FUNDS_MOVEMENT_INTENT":
                raise ValueError(
                    "Only funds movement intents can be confirmed."
                )

            if transfer.status not in {
                "FUNDS_INTENT_CREATED",
                "FUNDS_FAILED"
            }:
                raise ValueError(
                    f"Funds movement cannot be confirmed from status: {transfer.status}"
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "transfer_id": command.transfer_id,
                "merchant_id": command.merchant_id,
                "provider_reference":
                    _normalize_optional_text(command.provider_reference),
                "external_reference":
                    _normalize_optional_text(command.external_reference),
                "railone_intent_id":
                    _normalize_optional_text(command.railone_intent_id),
                "reconciliation_state":
                    command.reconciliation_state.strip().upper(),
                "status": "FUNDS_CONFIRMED"
            }

            event = create_event(
                EventType.TRANSFER_FUNDS_CONFIRMED,
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
                "transfer_id": command.transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "FUNDS_CONFIRMED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class FailFundsMovementCommandHandler:
    def handle(self, command: FailFundsMovementCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "transfer_id": command.transfer_id,
                "expected_version": command.expected_version,
                "reason": command.reason,
                "provider_reference": command.provider_reference,
                "external_reference": command.external_reference,
                "railone_intent_id": command.railone_intent_id
            }
        )

        aggregate_id = _transfer_aggregate_id(
            command.transfer_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="FailFundsMovementCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            transfer = _get_transfer_projection(
                uow.db,
                command.merchant_id,
                command.transfer_id
            )

            if not transfer:
                raise ValueError(
                    "Transfer not found."
                )

            if transfer.transfer_type != "FUNDS_MOVEMENT_INTENT":
                raise ValueError(
                    "Only funds movement intents can fail."
                )

            if transfer.status not in {
                "FUNDS_INTENT_CREATED",
                "FUNDS_CONFIRMED"
            }:
                raise ValueError(
                    f"Funds movement cannot be failed from status: {transfer.status}"
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "transfer_id": command.transfer_id,
                "merchant_id": command.merchant_id,
                "reason": command.reason,
                "provider_reference":
                    _normalize_optional_text(command.provider_reference),
                "external_reference":
                    _normalize_optional_text(command.external_reference),
                "railone_intent_id":
                    _normalize_optional_text(command.railone_intent_id),
                "status": "FUNDS_FAILED"
            }

            event = create_event(
                EventType.TRANSFER_FUNDS_FAILED,
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
                "transfer_id": command.transfer_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "FUNDS_FAILED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response