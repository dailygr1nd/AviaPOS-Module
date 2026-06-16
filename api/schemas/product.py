from pydantic import BaseModel


class ProductCreateRequest(

    BaseModel

):

    merchant_id: str

    sku: str

    name: str

    price: float