from fastapi import APIRouter

from app_context import store

from modules.debts.service import (
    create_debt
)

router = APIRouter(

    prefix="/debts",

    tags=["Debts"]
)

@router.post("/")
def debt_create(data: dict):

    previous_hash = (

        store.latest_hash(

            data["merchant_id"]

        )

    )

    event = create_debt(

        merchant_id=
            data["merchant_id"],

        customer_id=
            data["customer_id"],

        amount=
            data["amount"],

        currency=
            data["currency"],

        due_date=
            data["due_date"],

        previous_hash=
            previous_hash
    )

    store.append(event)

    return {

        "success": True
    }