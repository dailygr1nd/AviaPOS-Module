from fastapi import APIRouter

from modules.suppliers.schemas import (
    CreateSupplierRequest
)

from modules.suppliers.service import (
    create_supplier
)


router = APIRouter()


@router.post("/")
def create_supplier_route(payload: CreateSupplierRequest):

    return create_supplier(**payload.dict())