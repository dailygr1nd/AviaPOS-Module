from datetime import datetime

from infrastructure.projections.base_projector import BaseProjector
from modules.payment_capture.models import PaymentCaptureProjection


class PaymentCaptureProjector(BaseProjector):
    projection_name = "payment_capture_projection"

    def __init__(self, db):
        self.db = db

    def handle(self, event):
        if event.event_type == "PAYMENT_CAPTURE_RECEIVED":
            self.capture_received(event)

        elif event.event_type == "PAYMENT_CAPTURE_MATCHED":
            self.capture_matched(event)

        elif event.event_type == "PAYMENT_CAPTURE_RECONCILED":
            self.capture_reconciled(event)

        elif event.event_type == "PAYMENT_CAPTURE_FAILED":
            self.capture_failed(event)

    def capture_received(self, event):
        payload = event.payload

        existing = (
            self.db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.capture_id
                == payload["capture_id"]
            )
            .first()
        )

        if existing:
            return

        row = PaymentCaptureProjection(
            capture_id=payload["capture_id"],
            merchant_id=payload["merchant_id"],
            branch_id=payload.get("branch_id"),
            provider=payload["provider"],
            provider_channel=payload["provider_channel"],
            provider_reference=payload["provider_reference"],
            external_reference=payload.get("external_reference"),
            payer_reference=payload.get("payer_reference"),
            payer_name=payload.get("payer_name"),
            amount=payload["amount"],
            currency=payload["currency"],
            payment_method=payload["payment_method"],
            reference_type=payload.get("reference_type"),
            reference_id=payload.get("reference_id"),
            railone_intent_id=payload.get("railone_intent_id"),
            status=payload.get("status", "CAPTURED"),
            reconciliation_state=payload.get(
                "reconciliation_state",
                "PENDING"
            ),
            raw_payload=payload.get("raw_payload", {}),
            capture_metadata=payload.get("metadata", {}),
            version=event.version,
            received_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(row)
        self.db.commit()

    def capture_matched(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["capture_id"]
        )

        if not row:
            return

        row.reference_type = payload["reference_type"]
        row.reference_id = payload["reference_id"]
        row.status = "MATCHED"
        row.reconciliation_state = "MATCHED"
        row.notes = payload.get("notes")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def capture_reconciled(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["capture_id"]
        )

        if not row:
            return

        row.status = "RECONCILED"
        row.reconciliation_state = payload.get(
            "reconciliation_state",
            "RECONCILED"
        )

        if payload.get("provider_reference"):
            row.provider_reference = payload["provider_reference"]

        if payload.get("external_reference"):
            row.external_reference = payload["external_reference"]

        if payload.get("railone_intent_id"):
            row.railone_intent_id = payload["railone_intent_id"]

        if payload.get("payment_id"):
            row.payment_id = payload["payment_id"]

        row.notes = payload.get("notes")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def capture_failed(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["capture_id"]
        )

        if not row:
            return

        row.status = "FAILED"
        row.reconciliation_state = "FAILED"
        row.reason = payload.get("reason")

        if payload.get("provider_reference"):
            row.provider_reference = payload["provider_reference"]

        if payload.get("external_reference"):
            row.external_reference = payload["external_reference"]

        if payload.get("railone_intent_id"):
            row.railone_intent_id = payload["railone_intent_id"]

        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def _get_row(
        self,
        merchant_id: str,
        capture_id: str
    ):
        return (
            self.db.query(PaymentCaptureProjection)
            .filter(
                PaymentCaptureProjection.merchant_id == merchant_id,
                PaymentCaptureProjection.capture_id == capture_id
            )
            .first()
        )