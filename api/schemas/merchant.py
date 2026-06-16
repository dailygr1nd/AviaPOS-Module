from pydantic import (
    BaseModel,
    EmailStr
)

class CreateMerchantRequest(

    BaseModel

):

    merchant_name: str

    owner_name: str

    phone: str

    email: EmailStr