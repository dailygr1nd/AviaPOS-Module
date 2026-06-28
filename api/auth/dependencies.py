from dataclasses import dataclass

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from jwt import ExpiredSignatureError
from jwt import InvalidTokenError

from api.auth.security import (
    decode_token
)

from core.permissions.roles import (
    Role
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


@dataclass
class AuthenticatedUser:

    user_id: str

    merchant_id: str

    role: str

    branch_id: str | None = None


def get_current_user(

    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    )

) -> AuthenticatedUser:

    if credentials is None:

        raise HTTPException(

            status_code=401,

            detail="Missing authorization token."

        )

    try:

        payload = decode_token(
            credentials.credentials
        )

    except ExpiredSignatureError:

        raise HTTPException(

            status_code=401,

            detail="Token has expired."

        )

    except InvalidTokenError:

        raise HTTPException(

            status_code=401,

            detail="Invalid token."

        )

    user_id = payload.get(
        "sub"
    )

    merchant_id = payload.get(
        "merchant_id"
    )

    role = payload.get(
        "role"
    )

    if not user_id or not merchant_id or not role:

        raise HTTPException(

            status_code=401,

            detail="Invalid token payload."

        )

    return AuthenticatedUser(

        user_id=user_id,

        merchant_id=merchant_id,

        role=role,

        branch_id=payload.get(
            "branch_id"
        )

    )


def require_roles(
    allowed_roles: list[Role]
):

    def dependency(

        current_user: AuthenticatedUser = Depends(
            get_current_user
        )

    ):

        if current_user.role not in [

            role.value

            for role in allowed_roles

        ]:

            raise HTTPException(

                status_code=403,

                detail="Insufficient permissions."

            )

        return current_user

    return dependency


def require_merchant_scope(

    merchant_id: str,

    current_user: AuthenticatedUser

):

    if merchant_id != current_user.merchant_id:

        raise HTTPException(

            status_code=403,

            detail="Merchant scope violation."

        )


def get_merchant_id(

    current_user: AuthenticatedUser = Depends(
        get_current_user
    )

):

    return current_user.merchant_id


def get_optional_merchant_id_header(

    x_merchant_id: str | None = Header(
        default=None
    )

):

    return x_merchant_id