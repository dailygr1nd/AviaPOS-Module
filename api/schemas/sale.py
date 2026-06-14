from pydantic import (
    BaseModel,
    Field
)

from typing import List

class SaleItem(

    BaseModel

):

    sku: str

    quantity: int = Field(
        gt=0
    )

    unit_price: float = Field(
        gt=0
    )

class CreateSaleRequest(

    BaseModel

):

    merchant_id: str

    amount: float = Field(
        gt=0
    )

    currency: str

    payment_method: str

    items: List[SaleItem]