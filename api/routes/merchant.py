from fastapi import (
    APIRouter
)

from app_context import (
    store
)

from modules.merchant.service import (
    create_merchant
)

from api.schemas.merchant import (
    CreateMerchantRequest
)

router = APIRouter(

    prefix="/merchant",

    tags=["Merchant"]
)

@router.post("/")
def merchant_create(

    data:
        CreateMerchantRequest

):

    merchant_id, event = (

        create_merchant(

            merchant_name=
                data.merchant_name,

            owner_name=
                data.owner_name,

            phone=
                data.phone,

            email=
                data.email
        )

    )

    store.append(event)

    return {

        "merchant_id":
            merchant_id
    }