from fastapi import APIRouter

from api.schemas.product import (
    ProductCreateRequest
)

from application.products.product_app_service import (
    ProductApplicationService
)

router = APIRouter()

service = ProductApplicationService()


@router.post("/")

def create_product(

    request:

    ProductCreateRequest

):

    event = service.create_product(

        merchant_id=
            request.merchant_id,

        sku=
            request.sku,

        name=
            request.name,

        price=
            request.price

    )

    return {

        "event_id":

            event.event_id,

        "event_type":

            event.event_type
    }