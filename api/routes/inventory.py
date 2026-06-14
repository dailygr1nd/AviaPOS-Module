from fastapi import APIRouter

from app_context import store

from modules.inventory.service import (
    receive_stock
)

router = APIRouter(

    prefix="/inventory",

    tags=["Inventory"]

)

@router.post("/receive")
def stock_receive(data: dict):

    previous_hash = (

        store.latest_hash(

            data["merchant_id"]

        )

    )

    event = receive_stock(

        merchant_id=
            data["merchant_id"],

        sku=data["sku"],

        quantity=
            data["quantity"],

        previous_hash=
            previous_hash
    )

    store.append(event)

    return {

        "success": True
    }