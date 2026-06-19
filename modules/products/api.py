from fastapi import APIRouter

from modules.products.schemas import (
    CreateProductRequest
)

from modules.products.service import (
    create_product
)


router = APIRouter()


@router.post("/")
def create_product_route(payload: CreateProductRequest):

    return create_product(**payload.dict())