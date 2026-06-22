from sqlalchemy.orm import Session

from modules.inventory.models import (
    InventoryProjection
)

from infrastructure.projections.base_projector import (
    BaseProjector
)


class InventoryProjector(
    BaseProjector
):

    projection_name = (
        "inventory_projection"
    )

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def handle(
        self,
        event
    ):

        payload = event.payload

        if event.event_type == (
            "INVENTORY_RECEIVED"
        ):

            self.receive(
                payload
            )

        elif event.event_type == (
            "INVENTORY_DEDUCTED"
        ):

            self.deduct(
                payload
            )

    def receive(
        self,
        payload
    ):

        row = (

            self.db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.branch_id
                == payload["branch_id"],

                InventoryProjection.product_id
                == payload["product_id"]

            )

            .first()

        )

        if not row:

            row = InventoryProjection(

                branch_id=
                    payload["branch_id"],

                product_id=
                    payload["product_id"],

                quantity=0

            )

            self.db.add(row)

        row.quantity += (
            payload["quantity"]
        )

        self.db.commit()

    def deduct(
        self,
        payload
    ):

        row = (

            self.db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.branch_id
                == payload["branch_id"],

                InventoryProjection.product_id
                == payload["product_id"]

            )

            .first()

        )

        if not row:
            return

        row.quantity -= (
            payload["quantity"]
        )

        self.db.commit()