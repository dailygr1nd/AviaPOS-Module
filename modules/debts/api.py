from fastapi import APIRouter

from modules.debts.schemas import (
    CreateDebtRequest,
    RecordPaymentRequest
)

from modules.debts.service import (
    create_debt,
    record_payment
)


router = APIRouter()


@router.post("/")
def create_debt_route(payload: CreateDebtRequest):

    return create_debt(**payload.dict())


@router.post("/payment")
def record_payment_route(payload: RecordPaymentRequest):

    return record_payment(**payload.dict())