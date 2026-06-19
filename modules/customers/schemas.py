from pydantic import BaseModel
from typing import Optional


class CreateCustomerRequest(BaseModel):

    merchant_id: str
    customer_id: str
    name: str
    phone: Optional[str] = None