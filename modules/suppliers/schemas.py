from pydantic import BaseModel


class CreateSupplierRequest(BaseModel):

    merchant_id: str
    supplier_id: str
    name: str
    phone: str = ""