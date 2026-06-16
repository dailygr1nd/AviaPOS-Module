from pydantic import BaseModel


class SaleCreateRequest(

    BaseModel

):

    merchant_id: str

    product_id: str

    quantity: int

    amount: float

    currency: str