from fastapi import Header

from typing import Optional


def get_merchant_id(

    x_merchant_id:

    Optional[str] = Header(

        default=None

    )

):

    return x_merchant_id