from infrastructure.database.session import (
    SessionLocal
)

from modules.inventory.models import (
    InventoryProjection
)


def _serialize_inventory(
    row: InventoryProjection
):

    return {

        "merchant_id":
            row.merchant_id,

        "branch_id":
            row.branch_id,

        "product_id":
            row.product_id,

        "sku":
            row.sku,

        "quantity":
            row.quantity,

        "last_cost_price":
            row.last_cost_price,

        "version":
            row.version,

        "updated_at":
            row.updated_at

    }


def get_inventory(
    merchant_id: str
):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.merchant_id
                == merchant_id
            )

            .order_by(
                InventoryProjection.updated_at.desc()
            )

            .all()

        )

        return [

            _serialize_inventory(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_branch_inventory(

    merchant_id: str,

    branch_id: str

):

    db = SessionLocal()

    try:

        rows = (

            db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.merchant_id
                == merchant_id,

                InventoryProjection.branch_id
                == branch_id

            )

            .order_by(
                InventoryProjection.updated_at.desc()
            )

            .all()

        )

        return [

            _serialize_inventory(
                row
            )

            for row in rows

        ]

    finally:

        db.close()


def get_product_inventory(

    merchant_id: str,

    branch_id: str,

    product_id: str

):

    db = SessionLocal()

    try:

        row = (

            db.query(
                InventoryProjection
            )

            .filter(
                InventoryProjection.merchant_id
                == merchant_id,

                InventoryProjection.branch_id
                == branch_id,

                InventoryProjection.product_id
                == product_id

            )

            .first()

        )

        if not row:

            return None

        return _serialize_inventory(
            row
        )

    finally:

        db.close()