from fastapi import APIRouter

from modules.inventory.schemas import (
    ReceiveStockRequest,
    DeductStockRequest
)

from modules.inventory.service import (
    receive_stock,
    deduct_stock
)


router = APIRouter()


@router.post("/receive")
def receive_stock_route(payload: ReceiveStockRequest):

    return receive_stock(**payload.dict())


@router.post("/deduct")
def deduct_stock_route(payload: DeductStockRequest):

    return deduct_stock(**payload.dict())