from sqlalchemy import or_

from infrastructure.database.session import SessionLocal
from modules.branches.models import BranchProjection


def _serialize_branch(row: BranchProjection):
    return {
        "branch_id": row.branch_id,
        "merchant_id": row.merchant_id,
        "branch_code": row.branch_code,
        "name": row.name,
        "location": row.location,
        "phone": row.phone,
        "address": row.address,
        "manager_user_id": row.manager_user_id,
        "active": row.active,
        "version": row.version,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }


def get_branches(
    merchant_id: str,
    include_inactive: bool = False
):
    db = SessionLocal()

    try:
        query = (
            db.query(BranchProjection)
            .filter(
                BranchProjection.merchant_id == merchant_id
            )
        )

        if not include_inactive:
            query = query.filter(
                BranchProjection.active == True
            )

        rows = (
            query.order_by(
                BranchProjection.name.asc()
            )
            .all()
        )

        return [
            _serialize_branch(row)
            for row in rows
        ]

    finally:
        db.close()


def get_branch(
    merchant_id: str,
    branch_id: str
):
    db = SessionLocal()

    try:
        row = (
            db.query(BranchProjection)
            .filter(
                BranchProjection.merchant_id == merchant_id,
                BranchProjection.branch_id == branch_id
            )
            .first()
        )

        if not row:
            return None

        return _serialize_branch(row)

    finally:
        db.close()


def search_branches(
    merchant_id: str,
    query_text: str,
    include_inactive: bool = False
):
    db = SessionLocal()

    try:
        like_value = f"%{query_text}%"

        query = (
            db.query(BranchProjection)
            .filter(
                BranchProjection.merchant_id == merchant_id
            )
            .filter(
                or_(
                    BranchProjection.name.ilike(like_value),
                    BranchProjection.location.ilike(like_value),
                    BranchProjection.branch_code.ilike(like_value)
                )
            )
        )

        if not include_inactive:
            query = query.filter(
                BranchProjection.active == True
            )

        rows = (
            query.order_by(
                BranchProjection.name.asc()
            )
            .limit(50)
            .all()
        )

        return [
            _serialize_branch(row)
            for row in rows
        ]

    finally:
        db.close()