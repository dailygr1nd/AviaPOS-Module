from pydantic import BaseModel


class InventoryReceiptRequest(

    BaseModel

):

    merchant_id: str

    product_id: str

    sku: str

    quantity: int

    cost_price: float