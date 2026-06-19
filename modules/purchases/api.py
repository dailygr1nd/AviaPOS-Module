from fastapi import APIRouter

from modules.purchases.schemas import (
    CreatePurchaseOrderRequest,
    ReceivePurchaseRequest
)

from modules.purchases.service import (
    create_purchase_order,
    receive_purchase
)

router = APIRouter()


@router.post("/order")
def create_order(payload: CreatePurchaseOrderRequest):

    return create_purchase_order(

        merchant_id=payload.merchant_id,

        supplier_id=payload.supplier_id,

        items=[item.dict() for item in payload.items]

    )


@router.post("/receive")
def receive(payload: ReceivePurchaseRequest):

    return receive_purchase(

        merchant_id=payload.merchant_id,

        purchase_id=payload.purchase_id,

        items=[item.dict() for item in payload.items]

    )