from pydantic import BaseModel
from typing import List


class PurchaseItem(BaseModel):

    product_id: str
    sku: str
    quantity: int
    cost_price: float


class CreatePurchaseOrderRequest(BaseModel):

    merchant_id: str
    supplier_id: str
    items: List[PurchaseItem]


class ReceivePurchaseRequest(BaseModel):

    merchant_id: str
    purchase_id: str
    items: List[PurchaseItem]