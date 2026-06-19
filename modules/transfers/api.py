from fastapi import APIRouter

from modules.transfers.schemas import (
    CreateTransferRequest,
    SettleTransferRequest
)

from modules.transfers.service import (
    create_transfer,
    settle_transfer
)

router = APIRouter()


@router.post("/")
def create(payload: CreateTransferRequest):

    return create_transfer(

        merchant_id=payload.merchant_id,

        source_branch_id=payload.source_branch_id,

        destination_branch_id=payload.destination_branch_id,

        product_id=payload.product_id,

        sku=payload.sku,

        quantity=payload.quantity

    )


@router.post("/settle")
def settle(payload: SettleTransferRequest):

    return settle_transfer(

        merchant_id=payload.merchant_id,

        transfer_id=payload.transfer_id

    )