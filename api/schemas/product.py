from pydantic import (
    BaseModel,
    Field
)


class CreateProductRequest(

    BaseModel

):

    merchant_id: str

    sku: str = Field(
        min_length=1,
        max_length=64
    )

    name: str = Field(
        min_length=1,
        max_length=255
    )

    selling_price: float = Field(
        gt=0
    )

    cost_price: float = Field(
        ge=0
    )

    unit: str