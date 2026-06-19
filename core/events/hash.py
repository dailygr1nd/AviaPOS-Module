import hashlib
import json


def canonical_json(
    payload: dict
) -> str:

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    )


def calculate_payload_hash(
    payload: dict
) -> str:

    canonical = canonical_json(
        payload
    )

    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def calculate_event_hash(
    event_type: str,
    merchant_id: str,
    payload_hash: str,
    previous_hash: str
) -> str:

    data = "|".join([
        event_type,
        merchant_id,
        payload_hash,
        previous_hash
    ])

    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()