from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.projections.base_projector import (
    BaseProjector
)

from modules.inventory.models import (
    InventoryProjection
)


class InventoryProjector(
    BaseProjector
):

    projection_name = "inventory_projection"

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def handle(
        self,
        event
    ):

        if event.event_type == "INVENTORY_RECEIVED":

            self.receive(
                event
            )

        elif event.event_type == "INVENTORY_DEDUCTED":

            self.deduct(
                event
            )

        elif event.event_type == "INVENTORY_ADJUSTED":

            self.adjust(
                event
            )

    def _get_or_create_row(
        self,
        payload: dict
    ):

        row = (

            self.db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.merchant_id
                == payload["merchant_id"],

                InventoryProjection.branch_id
                == payload["branch_id"],

                InventoryProjection.product_id
                == payload["product_id"]

            )

            .first()

        )

        if row:

            return row

        row = InventoryProjection(

            merchant_id=
                payload["merchant_id"],

            branch_id=
                payload["branch_id"],

            product_id=
                payload["product_id"],

            sku=
                payload["sku"],

            quantity=0,

            last_cost_price=None,

            version=0,

            updated_at=datetime.utcnow()

        )

        self.db.add(
            row
        )

        return row

    def receive(
        self,
        event
    ):

        payload = event.payload

        row = self._get_or_create_row(
            payload
        )

        row.quantity += payload["quantity"]

        row.sku = payload["sku"]

        row.last_cost_price = payload.get(
            "cost_price"
        )

        row.version = event.version

        row.updated_at = datetime.utcnow()

        self.db.commit()

    def deduct(
        self,
        event
    ):

        payload = event.payload

        row = self._get_or_create_row(
            payload
        )

        row.quantity -= payload["quantity"]

        row.sku = payload["sku"]

        row.version = event.version

        row.updated_at = datetime.utcnow()

        self.db.commit()

    def adjust(
        self,
        event
    ):

        payload = event.payload

        row = self._get_or_create_row(
            payload
        )

        row.quantity += payload["adjustment"]

        row.sku = payload["sku"]

        row.version = event.version

        row.updated_at = datetime.utcnow()

        self.db.commit()