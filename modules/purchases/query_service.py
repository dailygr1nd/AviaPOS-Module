from infrastructure.database.session import SessionLocal
from modules.purchases.models import PurchaseProjection


def _serialize_purchase(row: PurchaseProjection):
    return {
        "purchase_id": row.purchase_id,
        "merchant_id": row.merchant_id,
        "branch_id": row.branch_id,
        "supplier_id": row.supplier_id,
        "supplier_invoice_ref": row.supplier_invoice_ref,
        "status": row.status,
        "total": row.total,
        "notes": row.notes,
        "lines": row.lines,
        "received_items": row.received_items,
        "received_by_user_id": row.received_by_user_id,
        "version": row.version,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }


def get_purchases(
    merchant_id: str,
    status: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.merchant_id == merchant_id
            )
        )

        if status:
            query = query.filter(
                PurchaseProjection.status == status.upper()
            )

        rows = (
            query.order_by(
                PurchaseProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_purchase(row)
            for row in rows
        ]

    finally:
        db.close()


def get_branch_purchases(
    merchant_id: str,
    branch_id: str,
    status: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.merchant_id == merchant_id,
                PurchaseProjection.branch_id == branch_id
            )
        )

        if status:
            query = query.filter(
                PurchaseProjection.status == status.upper()
            )

        rows = (
            query.order_by(
                PurchaseProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_purchase(row)
            for row in rows
        ]

    finally:
        db.close()


def get_supplier_purchases(
    merchant_id: str,
    supplier_id: str,
    status: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.merchant_id == merchant_id,
                PurchaseProjection.supplier_id == supplier_id
            )
        )

        if status:
            query = query.filter(
                PurchaseProjection.status == status.upper()
            )

        rows = (
            query.order_by(
                PurchaseProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_purchase(row)
            for row in rows
        ]

    finally:
        db.close()


def get_purchase(
    merchant_id: str,
    purchase_id: str
):
    db = SessionLocal()

    try:
        row = (
            db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.merchant_id == merchant_id,
                PurchaseProjection.purchase_id == purchase_id
            )
            .first()
        )

        if not row:
            return None

        return _serialize_purchase(row)

    finally:
        db.close()