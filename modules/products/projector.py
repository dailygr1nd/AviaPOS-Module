from datetime import datetime

from infrastructure.projections.base_projector import (
    BaseProjector
)

from modules.products.models import (
    ProductProjection
)


class ProductProjector(
    BaseProjector
):

    projection_name = "product_projection"

    def __init__(
        self,
        db
    ):

        self.db = db

    def handle(
        self,
        event
    ):

        if event.event_type == "PRODUCT_CREATED":

            self.create(
                event
            )

        elif event.event_type == "PRODUCT_UPDATED":

            self.update(
                event
            )

    def create(
        self,
        event
    ):

        payload = event.payload

        existing = (

            self.db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.product_id
                == payload["product_id"]
            )

            .first()

        )

        if existing:

            return

        row = ProductProjection(

            product_id=
                payload["product_id"],

            merchant_id=
                payload["merchant_id"],

            sku=
                payload["sku"],

            name=
                payload["name"],

            selling_price=
                payload["selling_price"],

            cost_price=
                payload["cost_price"],

            category=
                payload.get(
                    "category"
                ),

            barcode=
                payload.get(
                    "barcode"
                ),

            active=True,

            version=
                event.version,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow()

        )

        self.db.add(
            row
        )

        self.db.commit()

    def update(
        self,
        event
    ):

        payload = event.payload

        row = (

            self.db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.product_id
                == payload["product_id"],

                ProductProjection.merchant_id
                == payload["merchant_id"]

            )

            .first()

        )

        if not row:

            return

        for field in [

            "sku",

            "name",

            "selling_price",

            "cost_price",

            "category",

            "barcode",

            "active"

        ]:

            if field in payload:

                setattr(

                    row,

                    field,

                    payload[field]

                )

        row.version = event.version

        row.updated_at = datetime.utcnow()

        self.db.commit()