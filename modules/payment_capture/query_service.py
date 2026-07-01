from sqlalchemy import or_

from infrastructure.database.session import SessionLocal
from modules.payment_capture.models import PaymentCaptureProjection


def _serialize_capture(row: PaymentCaptureProjection):
    return {
        "capture_id": row.capture_id,
        "merchant_id": row.merchant_id,
        "branch_id": row.branch_id,
        "provider": row.provider,
        "provider_channel": row.provider_channel,
        "provider_reference": row.provider_reference,
        "external_reference": row.external_reference,
        "payer_reference": row.payer_reference,
        "payer_name": row.payer_name,
        "amount": row.amount,
        "currency": row.currency,
        "payment_method": row.payment_method,
        "reference_type": row.reference_type,
        "reference_id": row.reference_id,
        "payment_id": row.payment_id,
        "railone_intent_id": row.railone_intent_id,
        "status": row.status,
        "reconciliation_state": row.reconciliation_state,
        "reason": row.reason,
        "notes": row.notes,
        "raw_payload": row.raw_payload,
        "capture_metadata": row.capture_metadata,
        "version": row.version,
        "received_at": row.received_at,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }


def get_payment_captures(
    merchant_id: str,
    status: str | None = None,
    provider: str | None = None,
    reference_type: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.merchant_id == merchant_id
            )
        )

        if status:
            query = query.filter(
                PaymentCaptureProjection.status == status.upper()
            )

        if provider:
            query = query.filter(
                PaymentCaptureProjection.provider == provider.upper()
            )

        if reference_type:
            query = query.filter(
                PaymentCaptureProjection.reference_type
                == reference_type.upper()
            )

        rows = (
            query.order_by(
                PaymentCaptureProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_capture(row)
            for row in rows
        ]

    finally:
        db.close()


def get_branch_payment_captures(
    merchant_id: str,
    branch_id: str,
    status: str | None = None,
    provider: str | None = None
):
    db = SessionLocal()

    try:
        query = (
            db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.merchant_id == merchant_id,
                PaymentCaptureProjection.branch_id == branch_id
            )
        )

        if status:
            query = query.filter(
                PaymentCaptureProjection.status == status.upper()
            )

        if provider:
            query = query.filter(
                PaymentCaptureProjection.provider == provider.upper()
            )

        rows = (
            query.order_by(
                PaymentCaptureProjection.created_at.desc()
            )
            .all()
        )

        return [
            _serialize_capture(row)
            for row in rows
        ]

    finally:
        db.close()


def search_payment_captures(
    merchant_id: str,
    query_text: str
):
    db = SessionLocal()

    try:
        like_value = f"%{query_text}%"

        rows = (
            db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.merchant_id == merchant_id
            )
            .filter(
                or_(
                    PaymentCaptureProjection.provider_reference.ilike(
                        like_value
                    ),
                    PaymentCaptureProjection.external_reference.ilike(
                        like_value
                    ),
                    PaymentCaptureProjection.payer_reference.ilike(
                        like_value
                    ),
                    PaymentCaptureProjection.payer_name.ilike(
                        like_value
                    ),
                    PaymentCaptureProjection.railone_intent_id.ilike(
                        like_value
                    )
                )
            )
            .order_by(
                PaymentCaptureProjection.created_at.desc()
            )
            .limit(50)
            .all()
        )

        return [
            _serialize_capture(row)
            for row in rows
        ]

    finally:
        db.close()


def get_payment_capture(
    merchant_id: str,
    capture_id: str
):
    db = SessionLocal()

    try:
        row = (
            db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.merchant_id == merchant_id,
                PaymentCaptureProjection.capture_id == capture_id
            )
            .first()
        )

        if not row:
            return None

        return _serialize_capture(row)

    finally:
        db.close()