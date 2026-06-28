from datetime import datetime

from modules.receivables.models import (
    ReceivableProjection
)

from infrastructure.projections.base_projector import (
    BaseProjector
)


class ReceivableProjector(
    BaseProjector
):

    projection_name = (
        "receivable_projection"
    )

    def __init__(
        self,
        db
    ):

        self.db = db

    def handle(
        self,
        event
    ):

        if event.event_type == (
            "RECEIVABLE_CREATED"
        ):

            self.create(
                event
            )

        elif event.event_type == (
            "RECEIVABLE_PAYMENT_RECORDED"
        ):

            self.record_payment(
                event
            )

        elif event.event_type == (
            "RECEIVABLE_SETTLED"
        ):

            self.settle(
                event
            )

    def create(
        self,
        event
    ):

        payload = event.payload

        existing = (

            self.db.query(
                ReceivableProjection
            )

            .filter(
                ReceivableProjection.receivable_id
                == payload["receivable_id"]
            )

            .first()

        )

        if existing:

            return

        row = ReceivableProjection(

            receivable_id=
                payload["receivable_id"],

            merchant_id=
                payload["merchant_id"],

            branch_id=
                payload["branch_id"],

            customer_id=
                payload["customer_id"],

            sale_id=
                payload["sale_id"],

            amount=
                payload["amount"],

            paid_amount=0,

            balance=
                payload["amount"],

            status="OPEN",

            version=
                event.version,

            created_at=
                datetime.utcnow()

        )

        self.db.add(
            row
        )

        self.db.commit()

    def record_payment(
        self,
        event
    ):

        payload = event.payload

        row = (

            self.db.query(
                ReceivableProjection
            )

            .filter(
                ReceivableProjection.receivable_id
                == payload["receivable_id"]
            )

            .first()

        )

        if not row:

            return

        row.paid_amount += (
            payload["amount"]
        )

        row.balance = (

            row.amount

            -

            row.paid_amount

        )

        if row.balance <= 0:

            row.balance = 0

            row.status = "SETTLED"

        else:

            row.status = "OPEN"

        row.version = event.version

        self.db.commit()

    def settle(
        self,
        event
    ):

        payload = event.payload

        row = (

            self.db.query(
                ReceivableProjection
            )

            .filter(
                ReceivableProjection.receivable_id
                == payload["receivable_id"]
            )

            .first()

        )

        if not row:

            return

        row.balance = 0

        row.status = "SETTLED"

        row.version = event.version

        self.db.commit()