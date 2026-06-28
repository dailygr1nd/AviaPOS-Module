from sqlalchemy import or_

from infrastructure.database.session import SessionLocal
from modules.suppliers.models import SupplierProjection


def _serialize_supplier(row: SupplierProjection):
    return {
        "supplier_id": row.supplier_id,
        "merchant_id": row.merchant_id,
        "supplier_code": row.supplier_code,
        "name": row.name,
        "contact_person": row.contact_person,
        "phone": row.phone,
        "email": row.email,
        "address": row.address,
        "tax_id": row.tax_id,
        "payment_terms": row.payment_terms,
        "active": row.active,
        "version": row.version,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }


def get_suppliers(
    merchant_id: str,
    include_inactive: bool = False
):
    db = SessionLocal()

    try:
        query = (
            db.query(SupplierProjection)
            .filter(
                SupplierProjection.merchant_id == merchant_id
            )
        )

        if not include_inactive:
            query = query.filter(
                SupplierProjection.active == True
            )

        rows = (
            query.order_by(
                SupplierProjection.name.asc()
            )
            .all()
        )

        return [
            _serialize_supplier(row)
            for row in rows
        ]

    finally:
        db.close()


def get_supplier(
    merchant_id: str,
    supplier_id: str
):
    db = SessionLocal()

    try:
        row = (
            db.query(SupplierProjection)
            .filter(
                SupplierProjection.merchant_id == merchant_id,
                SupplierProjection.supplier_id == supplier_id
            )
            .first()
        )

        if not row:
            return None

        return _serialize_supplier(row)

    finally:
        db.close()


def search_suppliers(
    merchant_id: str,
    query_text: str,
    include_inactive: bool = False
):
    db = SessionLocal()

    try:
        like_value = f"%{query_text}%"

        query = (
            db.query(SupplierProjection)
            .filter(
                SupplierProjection.merchant_id == merchant_id
            )
            .filter(
                or_(
                    SupplierProjection.name.ilike(like_value),
                    SupplierProjection.supplier_code.ilike(like_value),
                    SupplierProjection.contact_person.ilike(like_value),
                    SupplierProjection.phone.ilike(like_value),
                    SupplierProjection.email.ilike(like_value),
                    SupplierProjection.tax_id.ilike(like_value)
                )
            )
        )

        if not include_inactive:
            query = query.filter(
                SupplierProjection.active == True
            )

        rows = (
            query.order_by(
                SupplierProjection.name.asc()
            )
            .limit(50)
            .all()
        )

        return [
            _serialize_supplier(row)
            for row in rows
        ]

    finally:
        db.close()