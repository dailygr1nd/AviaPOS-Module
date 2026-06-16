from fastapi import APIRouter

from api.schemas.sales import (

    SaleCreateRequest

)

router = APIRouter()


@router.post("/")

def create_sale(

    request:

    SaleCreateRequest

):

    return {

        "success": True,

        "amount":

            request.amount

    }