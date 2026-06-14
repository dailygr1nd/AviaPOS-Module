from pydantic import (
    BaseModel,
    Field
)

class CreateMerchantRequest(

    BaseModel

):

    merchant_name: str

    owner_name: str

    phone: str

    email: str | None = None