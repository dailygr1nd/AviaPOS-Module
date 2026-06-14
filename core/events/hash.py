import hashlib
import json


def canonical_json(payload: dict) -> str:

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    )


def calculate_payload_hash(
    payload: dict
) -> str:

    return hashlib.sha256(

        canonical_json(payload)
        .encode()

    ).hexdigest()