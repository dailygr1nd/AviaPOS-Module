import uuid

from core.events.types import EventType
from core.ledger.event_factory import create_event

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.idempotency.request_hash import calculate_request_hash

from modules.branches.models import BranchProjection
from modules.products.models import ProductProjection
from modules.purchases.commands import (
    CancelPurchaseCommand,
    CreatePurchaseCommand,
    ReceivePurchaseCommand
)
from modules.purchases.models import PurchaseProjection
from modules.suppliers.models import SupplierProjection


def _purchase_aggregate_id(purchase_id: str) -> str:
    return f"purchase:{purchase_id}"


def _require_idempotency_key(idempotency_key: str | None):
    if not idempotency_key:
        raise ValueError(
            "Idempotency-Key header is required."
        )


def _normalize_sku(sku: str) -> str:
    return sku.strip().upper()


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
            "Active branch not found."
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
            "Active supplier not found."
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


def _get_purchase_projection(
    db,
    merchant_id: str,
    purchase_id: str
):
    return (
        db.query(PurchaseProjection)
        .filter(
            PurchaseProjection.merchant_id == merchant_id,
            PurchaseProjection.purchase_id == purchase_id
        )
        .first()
    )


def _normalize_purchase_items(
    db,
    merchant_id: str,
    items
):
    if not items:
        raise ValueError(
            "Purchase must contain at least one item."
        )

    normalized_items = []
    total = 0

    for item in items:
        if item.quantity <= 0:
            raise ValueError(
                "Purchase item quantity must be greater than zero."
            )

        if item.unit_cost < 0:
            raise ValueError(
                "Purchase item unit_cost cannot be negative."
            )

        _ensure_product_exists(
            db,
            merchant_id,
            item.product_id
        )

        sku = _normalize_sku(
            item.sku
        )

        line_total = item.quantity * item.unit_cost

        normalized_items.append(
            {
                "product_id": item.product_id,
                "sku": sku,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost,
                "line_total": line_total
            }
        )

        total += line_total

    return normalized_items, total


def _normalize_receive_items(
    db,
    merchant_id: str,
    items
):
    if not items:
        raise ValueError(
            "Received purchase must contain at least one item."
        )

    normalized_items = []

    for item in items:
        if item.quantity <= 0:
            raise ValueError(
                "Received item quantity must be greater than zero."
            )

        if item.cost_price < 0:
            raise ValueError(
                "Received item cost_price cannot be negative."
            )

        if item.inventory_expected_version < 0:
            raise ValueError(
                "inventory_expected_version cannot be negative."
            )

        _ensure_product_exists(
            db,
            merchant_id,
            item.product_id
        )

        normalized_items.append(
            {
                "product_id": item.product_id,
                "sku": _normalize_sku(item.sku),
                "quantity": item.quantity,
                "cost_price": item.cost_price,
                "inventory_expected_version": item.inventory_expected_version
            }
        )

    return normalized_items


class CreatePurchaseCommandHandler:
    def handle(self, command: CreatePurchaseCommand):
        _require_idempotency_key(command.idempotency_key)

        purchase_id = command.purchase_id or str(uuid.uuid4())

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "supplier_id": command.supplier_id,
                "purchase_id": purchase_id,
                "supplier_invoice_ref": command.supplier_invoice_ref,
                "notes": command.notes,
                "items": [
                    item.__dict__
                    for item in command.items
                ]
            }
        )

        aggregate_id = _purchase_aggregate_id(
            purchase_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CreatePurchaseCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            _ensure_branch_exists(
                uow.db,
                command.merchant_id,
                command.branch_id
            )

            _ensure_supplier_exists(
                uow.db,
                command.merchant_id,
                command.supplier_id
            )

            normalized_items, total = _normalize_purchase_items(
                uow.db,
                command.merchant_id,
                command.items
            )

            payload = {
                "purchase_id": purchase_id,
                "merchant_id": command.merchant_id,
                "branch_id": command.branch_id,
                "supplier_id": command.supplier_id,
                "supplier_invoice_ref": command.supplier_invoice_ref,
                "notes": command.notes,
                "items": normalized_items,
                "total": total,
                "status": "CREATED"
            }

            event = create_event(
                EventType.PURCHASE_CREATED,
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
                "purchase_id": purchase_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "total": total
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class ReceivePurchaseCommandHandler:
    def handle(self, command: ReceivePurchaseCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "purchase_id": command.purchase_id,
                "expected_version": command.expected_version,
                "received_by_user_id": command.received_by_user_id,
                "items": [
                    item.__dict__
                    for item in command.items
                ]
            }
        )

        aggregate_id = _purchase_aggregate_id(
            command.purchase_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="ReceivePurchaseCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            purchase = _get_purchase_projection(
                uow.db,
                command.merchant_id,
                command.purchase_id
            )

            if not purchase:
                raise ValueError(
                    "Purchase not found."
                )

            if purchase.status != "CREATED":
                raise ValueError(
                    f"Purchase cannot be received from status: {purchase.status}"
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
                "purchase_id": command.purchase_id,
                "merchant_id": command.merchant_id,
                "branch_id": purchase.branch_id,
                "supplier_id": purchase.supplier_id,
                "items": normalized_items,
                "received_by_user_id": command.received_by_user_id,
                "status": "RECEIVED"
            }

            event = create_event(
                EventType.PURCHASE_RECEIVED,
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
                "purchase_id": command.purchase_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": event.version,
                "status": "RECEIVED"
            }

            uow.idempotency.complete(
                idempotency_record,
                response
            )

            return response


class CancelPurchaseCommandHandler:
    def handle(self, command: CancelPurchaseCommand):
        _require_idempotency_key(command.idempotency_key)

        if command.expected_version < 1:
            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(
            {
                "merchant_id": command.merchant_id,
                "purchase_id": command.purchase_id,
                "expected_version": command.expected_version,
                "reason": command.reason
            }
        )

        aggregate_id = _purchase_aggregate_id(
            command.purchase_id
        )

        with UnitOfWork() as uow:
            idempotency_record, is_new = uow.idempotency.start(
                merchant_id=command.merchant_id,
                idempotency_key=command.idempotency_key,
                command_name="CancelPurchaseCommand",
                request_hash=request_hash
            )

            if not is_new:
                return idempotency_record.response_payload

            purchase = _get_purchase_projection(
                uow.db,
                command.merchant_id,
                command.purchase_id
            )

            if not purchase:
                raise ValueError(
                    "Purchase not found."
                )

            if purchase.status != "CREATED":
                raise ValueError(
                    f"Purchase cannot be cancelled from status: {purchase.status}"
                )

            current_version = uow.events.assert_expected_version(
                merchant_id=command.merchant_id,
                aggregate_id=aggregate_id,
                expected_version=command.expected_version
            )

            next_version = current_version + 1

            payload = {
                "purchase_id": command.purchase_id,
                "merchant_id": command.merchant_id,
                "branch_id": purchase.branch_id,
                "supplier_id": purchase.supplier_id,
                "reason": command.reason,
                "status": "CANCELLED"
            }

            event = create_event(
                EventType.PURCHASE_CANCELLED,
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
                "purchase_id": command.purchase_id,
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