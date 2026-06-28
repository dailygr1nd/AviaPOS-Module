from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from core.permissions.roles import (
    Role
)


class BootstrapOwnerRequest(
    BaseModel
):

    merchant_id: str

    username: str = Field(
        min_length=3,
        max_length=100
    )

    password: str = Field(
        min_length=6
    )


class CreateUserRequest(
    BaseModel
):

    merchant_id: str

    username: str = Field(
        min_length=3,
        max_length=100
    )

    password: str = Field(
        min_length=6
    )

    role: Role

    branch_id: Optional[str] = None


class LoginRequest(
    BaseModel
):

    merchant_id: str

    username: str

    password: str


class AuthTokenResponse(
    BaseModel
):

    access_token: str

    token_type: str = "bearer"


class CurrentUserResponse(
    BaseModel
):

    user_id: str

    merchant_id: str

    username: str

    role: str

    branch_id: Optional[str] = None

    active: bool