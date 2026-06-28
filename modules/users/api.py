from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from api.auth.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_merchant_scope,
    require_roles
)

from core.permissions.roles import (
    Role
)

from modules.users.schemas import (
    BootstrapOwnerRequest,
    CreateUserRequest,
    LoginRequest
)

from modules.users.service import (
    bootstrap_owner,
    create_user,
    get_user_profile,
    login_user
)


router = APIRouter(

    prefix="/auth",

    tags=["Auth"]

)


@router.post("/bootstrap-owner")
def bootstrap_owner_route(
    request: BootstrapOwnerRequest
):

    return bootstrap_owner(

        merchant_id=
            request.merchant_id,

        username=
            request.username,

        password=
            request.password

    )


@router.post("/login")
def login(
    request: LoginRequest
):

    return login_user(

        merchant_id=
            request.merchant_id,

        username=
            request.username,

        password=
            request.password

    )


@router.get("/me")
def me(

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    return get_user_profile(
        current_user.user_id
    )


@router.post("/users")
def create_user_route(

    request: CreateUserRequest,

    current_user: AuthenticatedUser = Depends(

        require_roles(
            [
                Role.OWNER,
                Role.MANAGER
            ]
        )

    )

):

    require_merchant_scope(

        request.merchant_id,

        current_user

    )

    if current_user.role == Role.MANAGER.value:

        if request.role in [

            Role.OWNER,

            Role.MANAGER

        ]:

            raise HTTPException(

                status_code=403,

                detail="Managers cannot create owners or managers."

            )

    return create_user(

        merchant_id=
            request.merchant_id,

        username=
            request.username,

        password=
            request.password,

        role=
            request.role,

        branch_id=
            request.branch_id

    )