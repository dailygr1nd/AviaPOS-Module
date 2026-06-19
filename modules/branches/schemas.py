from pydantic import BaseModel


class CreateBranchRequest(BaseModel):

    merchant_id: str
    branch_id: str
    name: str
    location: str