from infrastructure.database.session import (
    SessionLocal
)

from modules.sales.models import (
    SaleProjection
)


def _serialize_sale(
    row: SaleProjection
):

    return {

        "sale_id":
            row.sale_id,

        "merchant_id":
            row.merchant_id,

        "branch_id":
            row.branch_id,

        "customer_id":
            row.customer_id,

        "payment_method":
            row.payment_method,

        "total":
            row.total,

        "status":
            row.status,

        "lines":
            row.lines or [],

        "version":
            row.version,

        "created_at":
            row.created_at,

        "updated_at":
            row.updated_at

    }


def get_sales(
    merchant_id: str
):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.merchant_id
                == merchant_id
            )

            .order_by(
                SaleProjection.created_at.desc()
            )

            .all()

        )

        return [

            _serialize_sale(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_branch_sales(

    merchant_id: str,

    branch_id: str

):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.merchant_id
                == merchant_id,

                SaleProjection.branch_id
                == branch_id

            )

            .order_by(
                SaleProjection.created_at.desc()
            )

            .all()

        )

        return [

            _serialize_sale(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_sale(

    merchant_id: str,

    sale_id: str

):

    db = SessionLocal()

    try:

        row = (

            db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.merchant_id
                == merchant_id,

                SaleProjection.sale_id
                == sale_id

            )

            .first()

        )

        if not row:

            return None

        return _serialize_sale(
            row
        )

    finally:

        db.close()


def get_sales_summary(
    merchant_id: str
):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                SaleProjection
            )

            .filter(
                SaleProjection.merchant_id
                == merchant_id
            )

            .all()

        )

        completed = [

            row

            for row in rows

            if row.status == "COMPLETED"

        ]

        cancelled = [

            row

            for row in rows

            if row.status == "CANCELLED"

        ]

        return {

            "total_sales_value":
                sum(
                    row.total
                    for row in completed
                ),

            "completed_count":
                len(
                    completed
                ),

            "cancelled_count":
                len(
                    cancelled
                ),

            "count":
                len(
                    rows
                )

        }

    finally:

        db.close()