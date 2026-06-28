from sqlalchemy import or_

from infrastructure.database.session import (
    SessionLocal
)

from modules.products.models import (
    ProductProjection
)


def _serialize_product(
    row: ProductProjection
):

    return {

        "product_id":
            row.product_id,

        "merchant_id":
            row.merchant_id,

        "sku":
            row.sku,

        "name":
            row.name,

        "selling_price":
            row.selling_price,

        "cost_price":
            row.cost_price,

        "category":
            row.category,

        "barcode":
            row.barcode,

        "active":
            row.active,

        "version":
            row.version,

        "created_at":
            row.created_at,

        "updated_at":
            row.updated_at

    }


def get_products(

    merchant_id: str,

    include_inactive: bool = False

):

    db = SessionLocal()

    try:

        query = (

            db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.merchant_id
                == merchant_id
            )

        )

        if not include_inactive:

            query = query.filter(
                ProductProjection.active
                == True
            )

        rows = (

            query.order_by(
                ProductProjection.name.asc()
            )

            .all()

        )

        return [

            _serialize_product(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_product(

    merchant_id: str,

    product_id: str

):

    db = SessionLocal()

    try:

        row = (

            db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.merchant_id
                == merchant_id,

                ProductProjection.product_id
                == product_id

            )

            .first()

        )

        if not row:

            return None

        return _serialize_product(
            row
        )

    finally:

        db.close()


def get_product_by_sku(

    merchant_id: str,

    sku: str

):

    db = SessionLocal()

    try:

        normalized_sku = sku.strip().upper()

        row = (

            db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.merchant_id
                == merchant_id,

                ProductProjection.sku
                == normalized_sku

            )

            .first()

        )

        if not row:

            return None

        return _serialize_product(
            row
        )

    finally:

        db.close()


def search_products(

    merchant_id: str,

    query_text: str,

    include_inactive: bool = False

):

    db = SessionLocal()

    try:

        like_value = f"%{query_text}%"

        query = (

            db.query(
                ProductProjection
            )

            .filter(
                ProductProjection.merchant_id
                == merchant_id
            )

            .filter(

                or_(

                    ProductProjection.name.ilike(
                        like_value
                    ),

                    ProductProjection.sku.ilike(
                        like_value
                    ),

                    ProductProjection.category.ilike(
                        like_value
                    ),

                    ProductProjection.barcode.ilike(
                        like_value
                    )

                )

            )

        )

        if not include_inactive:

            query = query.filter(
                ProductProjection.active
                == True
            )

        rows = (

            query.order_by(
                ProductProjection.name.asc()
            )

            .limit(
                50
            )

            .all()

        )

        return [

            _serialize_product(
                row
            )

            for row in rows

        ]

    finally:

        db.close()