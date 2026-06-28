from datetime import datetime

from infrastructure.projections.base_projector import (
    BaseProjector
)

from modules.sales.models import (
    SaleProjection
)


class SalesProjector(
    BaseProjector
):

    projection_name = "sale_projection"

    def __init__(
        self,
        db
    ):

        self.db = db

    def handle(
        self,
        event
    ):

        if event.event_type == "SALE_CREATED":

            self.create(
                event
            )

        elif event.event_type == "SALE_LINE_ADDED":

            self.add_line(
                event
            )

        elif event.event_type == "SALE_COMPLETED":

            self.complete(
                event
            )

        elif event.event_type == "SALE_CANCELLED":

            self.cancel(
                event
            )

    def create(
        self,
        event
    ):

        payload = event.payload

        existing = (

            self.db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.sale_id
                == payload["sale_id"]
            )

            .first()

        )

        if existing:

            return

        row = SaleProjection(

            sale_id=
                payload["sale_id"],

            merchant_id=
                payload["merchant_id"],

            branch_id=
                payload["branch_id"],

            customer_id=
                payload.get(
                    "customer_id"
                ),

            payment_method=
                payload["payment_method"],

            total=0,

            status="OPEN",

            lines=[],

            version=
                event.version,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow()

        )

        self.db.add(
            row
        )

        self.db.commit()

    def add_line(
        self,
        event
    ):

        payload = event.payload

        sale = (

            self.db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.sale_id
                == payload["sale_id"]
            )

            .first()

        )

        if not sale:

            return

        lines = list(
            sale.lines or []
        )

        line = {

            "product_id":
                payload["product_id"],

            "sku":
                payload["sku"],

            "quantity":
                payload["quantity"],

            "unit_price":
                payload["unit_price"],

            "line_total":
                payload["line_total"]

        }

        lines.append(
            line
        )

        sale.lines = lines

        sale.total += payload[
            "line_total"
        ]

        sale.version = event.version

        sale.updated_at = datetime.utcnow()

        self.db.commit()

    def complete(
        self,
        event
    ):

        payload = event.payload

        sale = (

            self.db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.sale_id
                == payload["sale_id"]
            )

            .first()

        )

        if not sale:

            return

        sale.status = "COMPLETED"

        sale.total = payload[
            "total"
        ]

        sale.version = event.version

        sale.updated_at = datetime.utcnow()

        self.db.commit()

    def cancel(
        self,
        event
    ):

        payload = event.payload

        sale = (

            self.db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.sale_id
                == payload["sale_id"]
            )

            .first()

        )

        if not sale:

            return

        sale.status = "CANCELLED"

        sale.version = event.version

        sale.updated_at = datetime.utcnow()

        self.db.commit()