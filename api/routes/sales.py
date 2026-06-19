from fastapi import APIRouter
from fastapi import HTTPException

from api.schemas.sales import (
    SaleCreateRequest
)

from application.sales.sales_app_service import (
    SalesApplicationService
)

router = APIRouter()

service = SalesApplicationService()


@router.post("/")
def create_sale(
    request: SaleCreateRequest
):
    try:

        result = service.create_sale(

            merchant_id=request.merchant_id,

            product_id=request.product_id,

            quantity=request.quantity,

            amount=request.amount,

            currency=request.currency

        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )