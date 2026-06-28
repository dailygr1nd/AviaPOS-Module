from sqlalchemy import or_

from infrastructure.database.session import SessionLocal
from modules.transfers.models import TransferProjection


def _serialize_transfer(row: TransferProjection):
    return {
        "transfer_id": row.transfer_id,
        "merchant_id": row.merchant_id,
        "transfer_type": row.transfer_type,
        "status": row.status,
        "source_branch_id": row.source_branch_id,
        "destination_branch_id": row.destination_branch_id,
        "destination_type": row.destination_type,
        "destination_reference": row.destination_reference,
        "amount": row.amount,
        "currency": row.currency,
        "purpose": row.purpose,
        "rail_hint": row.rail_hint,
        "external_reference": row.external_reference,
        "provider_reference": row.provider_reference,
        "railone_intent_id": row.railone_intent_id,
        "reconciliation_state": row.reconciliation_state,
        "notes": row.notes,
        "reason": row.reason,
        "items": row.items,
        "dispatched_items": row.dispatched_items,
        "received_items": row.received_items,
        "dispatched_by_user_id": row.dispatched_by_user_id,
        "received_by_user_id": row.received_by_user_id,
        "transfer_metadata": row.transfer_metadata,
        "version": row.version,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }


def get_transfers(
    merchant_id: str,
    transfer_type: str | None = None,
    status: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(TransferProjection)
            .filter(
                TransferProjection.merchant_id == merchant_id
            )
        )

        if transfer_type:
            query = query.filter(
                TransferProjection.transfer_type == transfer_type.upper()
            )

        if status:
            query = query.filter(
                TransferProjection.status == status.upper()
            )

        rows = (
            query.order_by(
                TransferProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_transfer(row)
            for row in rows
        ]

    finally:
        db.close()


def get_branch_transfers(
    merchant_id: str,
    branch_id: str,
    transfer_type: str | None = None,
    status: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(TransferProjection)
            .filter(
                TransferProjection.merchant_id == merchant_id
            )
            .filter(
                or_(
                    TransferProjection.source_branch_id == branch_id,
                    TransferProjection.destination_branch_id == branch_id
                )
            )
        )

        if transfer_type:
            query = query.filter(
                TransferProjection.transfer_type == transfer_type.upper()
            )

        if status:
            query = query.filter(
                TransferProjection.status == status.upper()
            )

        rows = (
            query.order_by(
                TransferProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_transfer(row)
            for row in rows
        ]

    finally:
        db.close()


def get_transfer(
    merchant_id: str,
    transfer_id: str
):
    db = SessionLocal()

    try:
        row = (
            db.query(TransferProjection)
            .filter(
                TransferProjection.merchant_id == merchant_id,
                TransferProjection.transfer_id == transfer_id
            )
            .first()
        )

        if not row:
            return None

        return _serialize_transfer(row)

    finally:
        db.close()