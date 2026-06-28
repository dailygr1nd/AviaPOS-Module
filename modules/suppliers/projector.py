from datetime import datetime

from infrastructure.projections.base_projector import BaseProjector
from modules.suppliers.models import SupplierProjection


class SupplierProjector(BaseProjector):
    projection_name = "supplier_projection"

    def __init__(self, db):
        self.db = db

    def handle(self, event):
        if event.event_type == "SUPPLIER_CREATED":
            self.create(event)

        elif event.event_type == "SUPPLIER_UPDATED":
            self.update(event)

    def create(self, event):
        payload = event.payload

        existing = (
            self.db.query(SupplierProjection)
            .filter(
                SupplierProjection.supplier_id == payload["supplier_id"]
            )
            .first()
        )

        if existing:
            return

        row = SupplierProjection(
            supplier_id=payload["supplier_id"],
            merchant_id=payload["merchant_id"],
            supplier_code=payload.get("supplier_code"),
            name=payload["name"],
            contact_person=payload.get("contact_person"),
            phone=payload.get("phone"),
            email=payload.get("email"),
            address=payload.get("address"),
            tax_id=payload.get("tax_id"),
            payment_terms=payload.get("payment_terms"),
            active=True,
            version=event.version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(row)
        self.db.commit()

    def update(self, event):
        payload = event.payload

        row = (
            self.db.query(SupplierProjection)
            .filter(
                SupplierProjection.supplier_id == payload["supplier_id"],
                SupplierProjection.merchant_id == payload["merchant_id"]
            )
            .first()
        )

        if not row:
            return

        for field in [
            "supplier_code",
            "name",
            "contact_person",
            "phone",
            "email",
            "address",
            "tax_id",
            "payment_terms",
            "active"
        ]:
            if field in payload:
                setattr(row, field, payload[field])

        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()