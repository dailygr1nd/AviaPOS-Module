from fastapi import APIRouter

from modules.control_center.trace import (
    trace_sale,
    trace_debt,
    trace_transfer
)

router = APIRouter()


@router.get("/trace/sale/{merchant_id}/{sale_id}")
def sale_trace(merchant_id: str, sale_id: str):

    return trace_sale(merchant_id, sale_id)


@router.get("/trace/debt/{merchant_id}/{debt_id}")
def debt_trace(merchant_id: str, debt_id: str):

    return trace_debt(merchant_id, debt_id)


@router.get("/trace/transfer/{merchant_id}/{transfer_id}")
def transfer_trace(merchant_id: str, transfer_id: str):

    return trace_transfer(merchant_id, transfer_id)