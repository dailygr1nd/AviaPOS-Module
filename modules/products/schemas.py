from pydantic import BaseModel


class CreateProductRequest(BaseModel):

    merchant_id: str
    product_id: str
    sku: str
    name: str
    selling_price: float
    cost_price: float