from infrastructure.database.session import (
    SessionLocal
)

from modules.receivables.models import (
    ReceivableProjection
)


def get_open_receivables(

    merchant_id: str

):

    db = SessionLocal()

    return (

        db.query(
            ReceivableProjection
        )

        .filter(
            ReceivableProjection.merchant_id
            == merchant_id
        )

        .all()

    )


def get_receivables_summary(

    merchant_id: str

):

    db = SessionLocal()

    rows = (

        db.query(
            ReceivableProjection
        )

        .filter(
            ReceivableProjection.merchant_id
            == merchant_id
        )

        .all()

    )

    outstanding = sum(
        x.balance
        for x in rows
    )

    return {

        "outstanding":
            outstanding,

        "count":
            len(rows)

    }