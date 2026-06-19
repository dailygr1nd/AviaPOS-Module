from fastapi import APIRouter

from modules.branches.schemas import (
    CreateBranchRequest
)

from modules.branches.service import (
    create_branch
)


router = APIRouter()


@router.post("/")
def create_branch_route(payload: CreateBranchRequest):

    return create_branch(**payload.dict())