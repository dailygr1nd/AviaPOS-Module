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
                event
            )

        elif event.event_type == (
            "PAYMENT_COMPLETED"
        ):

            self.complete(
                event
            )

        elif event.event_type == (
            "PAYMENT_FAILED"
        ):

            self.fail(
                event
            )

        elif event.event_type == (
            "PAYMENT_CANCELLED"
        ):

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
                PaymentProjection
            )

            .filter(
                PaymentProjection.payment_id
                == payload["payment_id"]
            )

            .first()

        )

        if existing:

            return

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

            version=
                event.version,

            created_at=
                datetime.utcnow()

        )

        self.db.add(
            row
        )

        self.db.commit()

    def complete(
        self,
        event
    ):

        self._update_status(

            payment_id=
                event.payload["payment_id"],

            status="COMPLETED",

            version=
                event.version

        )

    def fail(
        self,
        event
    ):

        self._update_status(

            payment_id=
                event.payload["payment_id"],

            status="FAILED",

            version=
                event.version

        )

    def cancel(
        self,
        event
    ):

        self._update_status(

            payment_id=
                event.payload["payment_id"],

            status="CANCELLED",

            version=
                event.version

        )

    def _update_status(

        self,

        payment_id: str,

        status: str,

        version: int

    ):

        payment = (

            self.db.query(
                PaymentProjection
            )

            .filter(
                PaymentProjection.payment_id
                == payment_id
            )

            .first()

        )

        if not payment:

            return

        payment.status = status

        payment.version = version

        self.db.commit()