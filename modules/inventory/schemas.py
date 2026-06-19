from pydantic import BaseModel
from typing import Optional


class ReceiveStockRequest(BaseModel):

    merchant_id: str
    branch_id: str
    product_id: str
    sku: str
    quantity: int
    cost_price: float


class DeductStockRequest(BaseModel):

    merchant_id: str
    branch_id: str
    product_id: str
    sku: str
    quantity: int
    reason: str