from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class CreateCustomerRequest(
    BaseModel
):

    merchant_id: str

    name: str = Field(
        min_length=1,
        max_length=255
    )

    customer_id: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[EmailStr] = None

    address: Optional[str] = None

    customer_type: str = "REGULAR"

    tax_id: Optional[str] = None

    credit_limit: float = Field(
        default=0,
        ge=0
    )


class UpdateCustomerRequest(
    BaseModel
):

    merchant_id: str

    customer_id: str

    name: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[EmailStr] = None

    address: Optional[str] = None

    customer_type: Optional[str] = None

    tax_id: Optional[str] = None

    credit_limit: Optional[float] = Field(
        default=None,
        ge=0
    )


class DeactivateCustomerRequest(
    BaseModel
):

    merchant_id: str

    customer_id: str

    reason: Optional[str] = None