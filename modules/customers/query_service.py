from sqlalchemy import or_

from infrastructure.database.session import (
    SessionLocal
)

from modules.customers.models import (
    CustomerProjection
)


def _serialize_customer(
    row: CustomerProjection
):

    return {

        "customer_id":
            row.customer_id,

        "merchant_id":
            row.merchant_id,

        "name":
            row.name,

        "phone":
            row.phone,

        "email":
            row.email,

        "address":
            row.address,

        "customer_type":
            row.customer_type,

        "tax_id":
            row.tax_id,

        "credit_limit":
            row.credit_limit,

        "active":
            row.active,

        "version":
            row.version,

        "created_at":
            row.created_at,

        "updated_at":
            row.updated_at

    }


def get_customers(

    merchant_id: str,

    include_inactive: bool = False

):

    db = SessionLocal()

    try:

        query = (

            db.query(
                CustomerProjection
            )

            .filter(
                CustomerProjection.merchant_id
                == merchant_id
            )

        )

        if not include_inactive:

            query = query.filter(
                CustomerProjection.active
                == True
            )

        rows = (

            query.order_by(
                CustomerProjection.name.asc()
            )

            .all()

        )

        return [

            _serialize_customer(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_customer(

    merchant_id: str,

    customer_id: str

):

    db = SessionLocal()

    try:

        row = (

            db.query(
                CustomerProjection
            )

            .filter(
                CustomerProjection.merchant_id
                == merchant_id,

                CustomerProjection.customer_id
                == customer_id

            )

            .first()

        )

        if not row:

            return None

        return _serialize_customer(
            row
        )

    finally:

        db.close()


def search_customers(

    merchant_id: str,

    query_text: str,

    include_inactive: bool = False

):

    db = SessionLocal()

    try:

        like_value = f"%{query_text}%"

        query = (

            db.query(
                CustomerProjection
            )

            .filter(
                CustomerProjection.merchant_id
                == merchant_id
            )

            .filter(

                or_(

                    CustomerProjection.name.ilike(
                        like_value
                    ),

                    CustomerProjection.phone.ilike(
                        like_value
                    ),

                    CustomerProjection.email.ilike(
                        like_value
                    ),

                    CustomerProjection.tax_id.ilike(
                        like_value
                    )

                )

            )

        )

        if not include_inactive:

            query = query.filter(
                CustomerProjection.active
                == True
            )

        rows = (

            query.order_by(
                CustomerProjection.name.asc()
            )

            .limit(
                50
            )

            .all()

        )

        return [

            _serialize_customer(
                row
            )

            for row in rows

        ]

    finally:

        db.close()