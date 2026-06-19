from fastapi import APIRouter

from modules.customers.schemas import (
    CreateCustomerRequest
)

from modules.customers.service import (
    create_customer
)


router = APIRouter()


@router.post("/")
def create_customer_route(payload: CreateCustomerRequest):

    return create_customer(**payload.dict())