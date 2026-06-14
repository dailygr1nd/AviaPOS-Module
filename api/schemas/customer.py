from pydantic import (
    BaseModel,
    Field
)


class CreateCustomerRequest(

    BaseModel

):

    merchant_id: str

    customer_id: str

    name: str = Field(
        min_length=1,
        max_length=255
    )

    phone: str