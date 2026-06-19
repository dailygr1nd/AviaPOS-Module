from fastapi import APIRouter

from core.ledger.store import (
    get_events_by_merchant
)

from modules.control_center.trace import trace_by_field

from modules.control_center.debug import get_snapshot

from modules.control_center.rebuild import rebuild


router = APIRouter()


# ---------------------------
# EVENT STREAM
# ---------------------------
@router.get("/events/{merchant_id}")
def events(merchant_id: str):

    return get_events_by_merchant(merchant_id)


# ---------------------------
# TRACE LAYER
# ---------------------------
@router.get("/trace/sale/{sale_id}")
def trace_sale(sale_id: str):

    return trace_by_field("sale_id", sale_id)


@router.get("/trace/debt/{debt_id}")
def trace_debt(debt_id: str):

    return trace_by_field("debt_id", debt_id)


@router.get("/trace/transfer/{transfer_id}")
def trace_transfer(transfer_id: str):

    return trace_by_field("transfer_id", transfer_id)


# ---------------------------
# DEBUG STATE
# ---------------------------
@router.get("/debug/state")
def debug_state():

    return get_snapshot()


# ---------------------------
# REBUILD ENGINE
# ---------------------------
@router.post("/debug/rebuild")
def rebuild_engine():

    return rebuild()