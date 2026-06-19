from fastapi import APIRouter

from api.schemas.inventory import (
    InventoryReceiptRequest
)

from application.inventory.inventory_app_service import (
    InventoryApplicationService
)

router = APIRouter()

service = InventoryApplicationService()


@router.post("/receive")
def receive_inventory(

    request:
    InventoryReceiptRequest

):

    event = service.create_stock_receipt(

        merchant_id=
            request.merchant_id,

        product_id=
            request.product_id,

        sku=
            request.sku,

        quantity=
            request.quantity,

        cost_price=
            request.cost_price

    )

    return {

        "event_id":
            event.event_id,

        "event_type":
            event.event_type
    }