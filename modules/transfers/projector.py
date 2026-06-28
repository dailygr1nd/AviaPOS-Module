from datetime import datetime

from infrastructure.projections.base_projector import BaseProjector
from modules.transfers.models import TransferProjection


class TransferProjector(BaseProjector):
    projection_name = "transfer_projection"

    def __init__(self, db):
        self.db = db

    def handle(self, event):
        if event.event_type == "TRANSFER_CREATED":
            self.create_stock_transfer(event)

        elif event.event_type == "TRANSFER_DISPATCHED":
            self.dispatch_stock_transfer(event)

        elif event.event_type == "TRANSFER_RECEIVED":
            self.receive_stock_transfer(event)

        elif event.event_type == "TRANSFER_CANCELLED":
            self.cancel_transfer(event)

        elif event.event_type == "TRANSFER_FUNDS_INTENT_CREATED":
            self.create_funds_intent(event)

        elif event.event_type == "TRANSFER_FUNDS_CONFIRMED":
            self.confirm_funds_movement(event)

        elif event.event_type == "TRANSFER_FUNDS_FAILED":
            self.fail_funds_movement(event)

    def create_stock_transfer(self, event):
        payload = event.payload

        existing = (
            self.db.query(TransferProjection)
            .filter(
                TransferProjection.transfer_id == payload["transfer_id"]
            )
            .first()
        )

        if existing:
            return

        row = TransferProjection(
            transfer_id=payload["transfer_id"],
            merchant_id=payload["merchant_id"],
            transfer_type="STOCK_TRANSFER",
            status="STOCK_CREATED",
            source_branch_id=payload["source_branch_id"],
            destination_branch_id=payload["destination_branch_id"],
            notes=payload.get("notes"),
            items=payload.get("items", []),
            dispatched_items=[],
            received_items=[],
            transfer_metadata={},
            version=event.version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(row)
        self.db.commit()

    def dispatch_stock_transfer(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["transfer_id"]
        )

        if not row:
            return

        row.status = "STOCK_DISPATCHED"
        row.dispatched_items = payload.get("items", [])
        row.dispatched_by_user_id = payload.get("dispatched_by_user_id")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def receive_stock_transfer(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["transfer_id"]
        )

        if not row:
            return

        row.status = "STOCK_RECEIVED"
        row.received_items = payload.get("items", [])
        row.received_by_user_id = payload.get("received_by_user_id")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def cancel_transfer(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["transfer_id"]
        )

        if not row:
            return

        row.status = "CANCELLED"
        row.reason = payload.get("reason")
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def create_funds_intent(self, event):
        payload = event.payload

        existing = (
            self.db.query(TransferProjection)
            .filter(
                TransferProjection.transfer_id == payload["transfer_id"]
            )
            .first()
        )

        if existing:
            return

        row = TransferProjection(
            transfer_id=payload["transfer_id"],
            merchant_id=payload["merchant_id"],
            transfer_type="FUNDS_MOVEMENT_INTENT",
            status="FUNDS_INTENT_CREATED",
            source_branch_id=payload.get("source_branch_id"),
            destination_branch_id=payload.get("destination_branch_id"),
            destination_type=payload["destination_type"],
            destination_reference=payload["destination_reference"],
            amount=payload["amount"],
            currency=payload["currency"],
            purpose=payload.get("purpose"),
            rail_hint=payload.get("rail_hint"),
            external_reference=payload.get("external_reference"),
            railone_intent_id=payload.get("railone_intent_id"),
            reconciliation_state="PENDING",
            transfer_metadata=payload.get("metadata", {}),
            version=event.version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(row)
        self.db.commit()

    def confirm_funds_movement(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["transfer_id"]
        )

        if not row:
            return

        row.status = "FUNDS_CONFIRMED"
        row.provider_reference = payload.get("provider_reference")
        row.external_reference = payload.get("external_reference")
        row.railone_intent_id = payload.get("railone_intent_id")
        row.reconciliation_state = payload.get(
            "reconciliation_state",
            "CONFIRMED"
        )
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def fail_funds_movement(self, event):
        payload = event.payload

        row = self._get_row(
            payload["merchant_id"],
            payload["transfer_id"]
        )

        if not row:
            return

        row.status = "FUNDS_FAILED"
        row.reason = payload.get("reason")
        row.provider_reference = payload.get("provider_reference")
        row.external_reference = payload.get("external_reference")
        row.railone_intent_id = payload.get("railone_intent_id")
        row.reconciliation_state = "FAILED"
        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()

    def _get_row(
        self,
        merchant_id: str,
        transfer_id: str
    ):
        return (
            self.db.query(TransferProjection)
            .filter(
                TransferProjection.merchant_id == merchant_id,
                TransferProjection.transfer_id == transfer_id
            )
            .first()
        )