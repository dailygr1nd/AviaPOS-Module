from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class SaleItem(
    BaseModel
):

    product_id: str

    sku: str

    quantity: int = Field(
        gt=0
    )

    unit_price: float = Field(
        gt=0
    )

    inventory_expected_version: int = Field(
        ge=1
    )


class CreateSaleRequest(
    BaseModel
):

    merchant_id: str

    branch_id: str

    items: List[SaleItem]

    payment_method: str

    customer_id: Optional[str] = None


class CreateSaleResponse(
    BaseModel
):

    success: bool

    sale_id: str

    total: float

    payment_method: str

    event_id: str

    event_type: str

    version: int