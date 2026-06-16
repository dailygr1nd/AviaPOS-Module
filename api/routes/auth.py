from fastapi import (
    APIRouter,
    HTTPException
)

from storage.sqlite.auth_repository import (
    AuthRepository
)

from api.schemas.auth import (

    LoginRequest,

    LoginResponse
)

from api.auth.security import (

    verify_password,

    create_access_token
)

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]
)

repo = AuthRepository(
    "aviapos.db"
)

@router.post(

    "/login",

    response_model=
        LoginResponse

)

def login(

    data:
        LoginRequest

):
        user = repo.get_user(

        data.username
    )

    if not user:

        raise HTTPException(

            status_code=401,

            detail=
                "Invalid credentials"
        )
    
valid = verify_password(

        data.password,

        user[
            "password_hash"
        ]
    )

if not valid:

        raise HTTPException(

            status_code=401,

            detail=
                "Invalid credentials"
        )

    token = (

        create_access_token(

            user["user_id"],

            user["merchant_id"],

            user["role"]
        )

    )

    return {

        "access_token":
            token,

        "token_type":
            "bearer"
    }