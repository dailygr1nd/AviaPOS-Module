from fastapi import (

    Depends
)

from api.auth.dependencies import (
    get_current_user
)

@router.get(
    "/{merchant_id}"
)
def dashboard(

    merchant_id: str,

    user=Depends(
        get_current_user
    )

):
    
    if (

    user["merchant_id"]

    !=

    merchant_id

):

    raise HTTPException(

        status_code=403,

        detail=
            "Forbidden"
    )