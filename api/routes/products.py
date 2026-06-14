from fastapi import APIRouter

from app_context import store

from modules.products.service import (
    create_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


from api.schemas.product import (
    CreateProductRequest
)

from api.schemas.common import (
    EventResponse
)

    previous_hash = (

        store.latest_hash(

            data["merchant_id"]

        )

    )

    event = create_product(

        merchant_id=
            data["merchant_id"],

        sku=data["sku"],

        name=data["name"],

        selling_price=
            data["selling_price"],

        cost_price=
            data["cost_price"],

        unit=data["unit"],

        previous_hash=
            previous_hash
    )

    store.append(event)

    return {

        "success": True,

        "event_id":
            event.event_id
    }