from fastapi import (

    Header,

    HTTPException
)

from api.auth.security import (
    decode_token
)

def get_current_user(

    authorization:
    str = Header(None)

):
    
        if not authorization:

        raise HTTPException(

            status_code=401,

            detail=
                "Missing token"
        )
    token = (

        authorization

        .replace(

            "Bearer ",

            ""

        )

    )

    try:

        return decode_token(
            token
        )

    except Exception:

        raise HTTPException(

            status_code=401,

            detail=
                "Invalid token"
        )