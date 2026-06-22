from datetime import datetime

from modules.payments.models import (
    PaymentProjection
)

from infrastructure.projections.base_projector import (
    BaseProjector
)


class PaymentProjector(
    BaseProjector
):

    projection_name = (
        "payment_projection"
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
            "PAYMENT_CREATED"
        ):

            self.create(
                event.payload
            )

        elif event.event_type == (
            "PAYMENT_COMPLETED"
        ):

            self.complete(
                event.payload
            )

        elif event.event_type == (
            "PAYMENT_FAILED"
        ):

            self.fail(
                event.payload
            )

    def create(
        self,
        payload
    ):

        row = PaymentProjection(

            payment_id=
                payload["payment_id"],

            merchant_id=
                payload["merchant_id"],

            amount=
                payload["amount"],

            payment_method=
                payload["payment_method"],

            reference_type=
                payload["reference_type"],

            reference_id=
                payload["reference_id"],

            status="PENDING",

            created_at=
                datetime.utcnow()

        )

        self.db.add(row)

        self.db.commit()

    def complete(
        self,
        payload
    ):

        payment = (

            self.db.query(
                PaymentProjection
            )

            .filter(
                PaymentProjection.payment_id
                ==
                payload["payment_id"]
            )

            .first()

        )

        if payment:

            payment.status = (
                "COMPLETED"
            )

            self.db.commit()

    def fail(
        self,
        payload
    ):

        payment = (

            self.db.query(
                PaymentProjection
            )

            .filter(
                PaymentProjection.payment_id
                ==
                payload["payment_id"]
            )

            .first()

        )

        if payment:

            payment.status = (
                "FAILED"
            )

            self.db.commit()