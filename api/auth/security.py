from datetime import (
    datetime,
    timedelta,
    timezone
)

import jwt

from passlib.context import (
    CryptContext
)

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"
)

SECRET_KEY = (
    "CHANGE_THIS_IN_PRODUCTION"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_MINUTES = 1440

def hash_password(

    password: str

):

    return pwd_context.hash(
        password
    )

def verify_password(

    password: str,

    hashed_password: str

):

    return pwd_context.verify(

        password,

        hashed_password
    )

def create_access_token(

    user_id: str,

    merchant_id: str,

    role: str

):

    expire = (

        datetime.now(
            timezone.utc
        )

        +

        timedelta(
            minutes=
            ACCESS_TOKEN_MINUTES
        )

    )

    payload = {

        "sub": user_id,

        "merchant_id":
            merchant_id,

        "role":
            role,

        "exp":
            expire
    }

    return jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=
        ALGORITHM
    )


def decode_token(

    token: str

):

    return jwt.decode(

        token,

        SECRET_KEY,

        algorithms=[
            ALGORITHM
        ]
    )