from datetime import datetime

from infrastructure.projections.base_projector import (
    BaseProjector
)

from modules.customers.models import (
    CustomerProjection
)


class CustomerProjector(
    BaseProjector
):

    projection_name = "customer_projection"

    def __init__(
        self,
        db
    ):

        self.db = db

    def handle(
        self,
        event
    ):

        if event.event_type == "CUSTOMER_CREATED":

            self.create(
                event
            )

        elif event.event_type == "CUSTOMER_UPDATED":

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
                CustomerProjection
            )

            .filter(
                CustomerProjection.customer_id
                == payload["customer_id"]
            )

            .first()

        )

        if existing:

            return

        row = CustomerProjection(

            customer_id=
                payload["customer_id"],

            merchant_id=
                payload["merchant_id"],

            name=
                payload["name"],

            phone=
                payload.get("phone"),

            email=
                payload.get("email"),

            address=
                payload.get("address"),

            customer_type=
                payload.get(
                    "customer_type",
                    "REGULAR"
                ),

            tax_id=
                payload.get("tax_id"),

            credit_limit=
                payload.get(
                    "credit_limit",
                    0
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
                CustomerProjection
            )

            .filter(
                CustomerProjection.customer_id
                == payload["customer_id"],

                CustomerProjection.merchant_id
                == payload["merchant_id"]

            )

            .first()

        )

        if not row:

            return

        for field in [

            "name",

            "phone",

            "email",

            "address",

            "customer_type",

            "tax_id",

            "credit_limit",

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