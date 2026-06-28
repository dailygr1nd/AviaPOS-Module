from datetime import datetime

from infrastructure.projections.base_projector import BaseProjector
from modules.purchases.models import PurchaseProjection


class PurchaseProjector(BaseProjector):
    projection_name = "purchase_projection"

    def __init__(self, db):
        self.db = db

    def handle(self, event):
        if event.event_type == "PURCHASE_CREATED":
            self.create(event)

        elif event.event_type == "PURCHASE_RECEIVED":
            self.receive(event)

        elif event.event_type == "PURCHASE_CANCELLED":
            self.cancel(event)

    def create(self, event):
        payload = event.payload

        existing = (
            self.db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.purchase_id == payload["purchase_id"]
            )
            .first()
        )

        if existing:
            return

        row = PurchaseProjection(
            purchase_id=payload["purchase_id"],
            merchant_id=payload["merchant_id"],
            branch_id=payload["branch_id"],
            supplier_id=payload["supplier_id"],
            supplier_invoice_ref=payload.get("supplier_invoice_ref"),
            status="CREATED",
            total=payload["total"],
            notes=payload.get("notes"),
            lines=payload.get("items", []),
            received_items=[],
            version=event.version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(row)
        self.db.commit()

    def receive(self, event):
        payload = event.payload

        row = (
            self.db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.purchase_id == payload["purchase_id"],
                PurchaseProjection.merchant_id == payload["merchant_id"]
            )
            .first()
        )

        if not row:
            return

        row.status = "RECEIVED"
        row.received_items = payload.get("items", [])
        row.received_by_user_id = payload.get("received_by_user_id")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def cancel(self, event):
        payload = event.payload

        row = (
            self.db.query(PurchaseProjection)
            .filter(
                PurchaseProjection.purchase_id == payload["purchase_id"],
                PurchaseProjection.merchant_id == payload["merchant_id"]
            )
            .first()
        )

        if not row:
            return

        row.status = "CANCELLED"
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()