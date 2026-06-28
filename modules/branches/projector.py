from datetime import datetime

from infrastructure.projections.base_projector import BaseProjector
from modules.branches.models import BranchProjection


class BranchProjector(BaseProjector):
    projection_name = "branch_projection"

    def __init__(self, db):
        self.db = db

    def handle(self, event):
        if event.event_type == "BRANCH_CREATED":
            self.create(event)

        elif event.event_type == "BRANCH_UPDATED":
            self.update(event)

    def create(self, event):
        payload = event.payload

        existing = (
            self.db.query(BranchProjection)
            .filter(
                BranchProjection.branch_id == payload["branch_id"]
            )
            .first()
        )

        if existing:
            return

        row = BranchProjection(
            branch_id=payload["branch_id"],
            merchant_id=payload["merchant_id"],
            branch_code=payload.get("branch_code"),
            name=payload["name"],
            location=payload["location"],
            phone=payload.get("phone"),
            address=payload.get("address"),
            manager_user_id=payload.get("manager_user_id"),
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
            self.db.query(BranchProjection)
            .filter(
                BranchProjection.branch_id == payload["branch_id"],
                BranchProjection.merchant_id == payload["merchant_id"]
            )
            .first()
        )

        if not row:
            return

        for field in [
            "branch_code",
            "name",
            "location",
            "phone",
            "address",
            "manager_user_id",
            "active"
        ]:
            if field in payload:
                setattr(row, field, payload[field])

        row.version = event.version
        row.updated_at = datetime.utcnow()

        self.db.commit()