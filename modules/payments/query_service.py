from infrastructure.database.session import (
    SessionLocal
)

from modules.payments.models import (
    PaymentProjection
)


def get_payments(

    merchant_id: str

):

    db = SessionLocal()

    return (

        db.query(
            PaymentProjection
        )

        .filter(
            PaymentProjection.merchant_id
            ==
            merchant_id
        )

        .all()

    )