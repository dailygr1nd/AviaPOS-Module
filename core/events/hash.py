import hashlib
import json


def canonical_json(payload: dict) -> str:

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    )


def calculate_payload_hash(

    payload

):

    data = json.dumps(

        payload,

        sort_keys=True

    )

    return hashlib.sha256(

        data.encode()

    ).hexdigest()