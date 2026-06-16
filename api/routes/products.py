from fastapi import APIRouter

from api.schemas.product import (

    ProductCreateRequest

)

router = APIRouter()


@router.post("/")

def create_product(

    request:

    ProductCreateRequest

):

    return {

        "success": True,

        "product_name":

            request.name

    }