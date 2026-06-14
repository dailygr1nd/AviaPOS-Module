from fastapi import APIRouter

from app_context import store

from modules.sales.service import (
    create_sale
)

router = APIRouter(

    prefix="/sales",

    tags=["Sales"]
)

@router.post("/")
def sale_create(data: dict):

    previous_hash = (

        store.latest_hash(

            data["merchant_id"]

        )

    )

    event = create_sale(

        merchant_id=
            data["merchant_id"],

        amount=
            data["amount"],

        currency=
            data["currency"],

        items=
            data["items"],

        payment_method=
            data["payment_method"],

        previous_hash=
            previous_hash
    )

    store.append(event)

    return {

        "success": True,

        "event_id":
            event.event_id
    }