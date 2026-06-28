import hashlib
import json


def calculate_request_hash(
    data: dict
) -> str:

    canonical = json.dumps(

        data,

        sort_keys=True,

        separators=(
            ",",
            ":"
        ),

        default=str

    )

    return hashlib.sha256(

        canonical.encode(
            "utf-8"
        )

    ).hexdigest()