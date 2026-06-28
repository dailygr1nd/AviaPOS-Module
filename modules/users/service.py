from fastapi import HTTPException

from api.auth.security import (
    create_access_token,
    hash_password,
    verify_password
)

from core.permissions.roles import (
    Role
)

from infrastructure.database.session import (
    SessionLocal
)

from modules.users.repository import (
    UserRepository
)


def _public_user(
    user
):

    return {

        "user_id":
            user.user_id,

        "merchant_id":
            user.merchant_id,

        "username":
            user.username,

        "role":
            user.role,

        "branch_id":
            user.branch_id,

        "active":
            user.active

    }


def bootstrap_owner(

    merchant_id: str,

    username: str,

    password: str

):

    db = SessionLocal()

    try:

        repo = UserRepository(
            db
        )

        existing_count = repo.count_merchant_users(
            merchant_id
        )

        if existing_count > 0:

            raise HTTPException(

                status_code=409,

                detail="Merchant already has users. Use normal user creation."

            )

        user = repo.create_user(

            merchant_id=merchant_id,

            username=username,

            password_hash=hash_password(
                password
            ),

            role=Role.OWNER.value,

            branch_id=None

        )

        return _public_user(
            user
        )

    finally:

        db.close()


def create_user(

    merchant_id: str,

    username: str,

    password: str,

    role: Role,

    branch_id: str | None = None

):

    db = SessionLocal()

    try:

        repo = UserRepository(
            db
        )

        existing = repo.get_by_username(

            merchant_id,

            username

        )

        if existing:

            raise HTTPException(

                status_code=409,

                detail="Username already exists for this merchant."

            )

        user = repo.create_user(

            merchant_id=merchant_id,

            username=username,

            password_hash=hash_password(
                password
            ),

            role=role.value,

            branch_id=branch_id

        )

        return _public_user(
            user
        )

    finally:

        db.close()


def login_user(

    merchant_id: str,

    username: str,

    password: str

):

    db = SessionLocal()

    try:

        repo = UserRepository(
            db
        )

        user = repo.get_by_username(

            merchant_id,

            username

        )

        if not user:

            raise HTTPException(

                status_code=401,

                detail="Invalid username or password."

            )

        if not user.active:

            raise HTTPException(

                status_code=403,

                detail="User account is inactive."

            )

        if not verify_password(

            password,

            user.password_hash

        ):

            raise HTTPException(

                status_code=401,

                detail="Invalid username or password."

            )

        token = create_access_token(

            user_id=user.user_id,

            merchant_id=user.merchant_id,

            role=user.role,

            branch_id=user.branch_id

        )

        return {

            "access_token":
                token,

            "token_type":
                "bearer"

        }

    finally:

        db.close()


def get_user_profile(
    user_id: str
):

    db = SessionLocal()

    try:

        repo = UserRepository(
            db
        )

        user = repo.get_by_user_id(
            user_id
        )

        if not user:

            raise HTTPException(

                status_code=404,

                detail="User not found."

            )

        return _public_user(
            user
        )

    finally:

        db.close()