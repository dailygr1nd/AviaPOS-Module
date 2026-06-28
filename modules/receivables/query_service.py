from infrastructure.database.session import (
    SessionLocal
)

from modules.receivables.models import (
    ReceivableProjection
)


def _serialize_receivable(
    row: ReceivableProjection
):

    return {

        "receivable_id":
            row.receivable_id,

        "merchant_id":
            row.merchant_id,

        "branch_id":
            row.branch_id,

        "customer_id":
            row.customer_id,

        "sale_id":
            row.sale_id,

        "amount":
            row.amount,

        "paid_amount":
            row.paid_amount,

        "balance":
            row.balance,

        "status":
            row.status,

        "version":
            row.version,

        "created_at":
            row.created_at

    }


def get_open_receivables(
    merchant_id: str
):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                ReceivableProjection
            )

            .filter(
                ReceivableProjection.merchant_id
                == merchant_id,

                ReceivableProjection.status
                == "OPEN"

            )

            .order_by(
                ReceivableProjection.created_at.desc()
            )

            .all()

        )

        return [

            _serialize_receivable(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_receivables_summary(
    merchant_id: str
):

    db = SessionLocal()

    try:

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
            row.balance
            for row in rows
        )

        total_original = sum(
            row.amount
            for row in rows
        )

        total_paid = sum(
            row.paid_amount
            for row in rows
        )

        open_count = sum(
            1
            for row in rows
            if row.status == "OPEN"
        )

        settled_count = sum(
            1
            for row in rows
            if row.status == "SETTLED"
        )

        return {

            "total_original":
                total_original,

            "total_paid":
                total_paid,

            "outstanding":
                outstanding,

            "count":
                len(
                    rows
                ),

            "open_count":
                open_count,

            "settled_count":
                settled_count

        }

    finally:

        db.close()