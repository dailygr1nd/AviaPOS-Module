from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class CreateProductRequest(
    BaseModel
):

    merchant_id: str

    sku: str = Field(
        min_length=1,
        max_length=100
    )

    name: str = Field(
        min_length=1,
        max_length=255
    )

    selling_price: float = Field(
        ge=0
    )

    cost_price: float = Field(
        ge=0
    )

    product_id: Optional[str] = None

    category: Optional[str] = None

    barcode: Optional[str] = None


class UpdateProductRequest(
    BaseModel
):

    merchant_id: str

    product_id: str

    sku: Optional[str] = None

    name: Optional[str] = None

    selling_price: Optional[float] = None

    cost_price: Optional[float] = None

    category: Optional[str] = None

    barcode: Optional[str] = None


class DeactivateProductRequest(
    BaseModel
):

    merchant_id: str

    product_id: str

    reason: Optional[str] = None