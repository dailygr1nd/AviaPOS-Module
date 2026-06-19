from fastapi import APIRouter

from modules.sales.schemas import (
    CreateSaleRequest,
    CreateSaleResponse
)

from modules.sales.service import create_sale


router = APIRouter()


@router.post("/", response_model=CreateSaleResponse)
def create_sale_route(payload: CreateSaleRequest):

    result = create_sale(

        merchant_id=payload.merchant_id,

        items=[item.dict() for item in payload.items],

        payment_method=payload.payment_method,

        customer_id=payload.customer_id

    )

    return CreateSaleResponse(**result)