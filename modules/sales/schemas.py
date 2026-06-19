from pydantic import BaseModel
from typing import List, Optional


class SaleItem(BaseModel):

    product_id: str
    sku: str
    quantity: int
    unit_price: float


class CreateSaleRequest(BaseModel):

    merchant_id: str
    items: List[SaleItem]
    payment_method: str
    customer_id: Optional[str] = None


class CreateSaleResponse(BaseModel):

    sale_id: str
    total: float
    payment_method: str