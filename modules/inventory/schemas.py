from pydantic import BaseModel


class ReceiveStockRequest(
    BaseModel
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    quantity: int

    cost_price: float


class DeductStockRequest(
    BaseModel
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    quantity: int

    reason: str


class AdjustStockRequest(
    BaseModel
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    adjustment: int

    reason: str