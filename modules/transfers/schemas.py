from pydantic import BaseModel


class CreateTransferRequest(BaseModel):

    merchant_id: str
    source_branch_id: str
    destination_branch_id: str
    product_id: str
    sku: str
    quantity: int


class SettleTransferRequest(BaseModel):

    merchant_id: str
    transfer_id: str