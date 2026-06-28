from fastapi import APIRouter
from fastapi import Depends

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope
)

from modules.dashboard.query_service import (
    get_dashboard_summary
)


router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)


@router.get("/{merchant_id}")
def merchant_dashboard(

    merchant_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_dashboard_summary(
        merchant_id=merchant_id
    )


@router.get("/{merchant_id}/branch/{branch_id}")
def branch_dashboard(

    merchant_id: str,

    branch_id: str,

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    require_merchant_scope(
        merchant_id,
        current_user
    )

    return get_dashboard_summary(

        merchant_id=merchant_id,

        branch_id=branch_id

    )