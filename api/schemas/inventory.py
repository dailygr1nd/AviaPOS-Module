from pydantic import (
    BaseModel,
    Field
)


class ReceiveStockRequest(

    BaseModel

):

    merchant_id: str

    sku: str

    quantity: int = Field(
        gt=0
    )