import hashlib

def calculate_event_hash(

    event_type: str,

    merchant_id: str,

    timestamp: str,

    previous_hash: str,

    payload_hash: str

):

    raw = (

        f"{event_type}"

        f"{merchant_id}"

        f"{timestamp}"

        f"{previous_hash}"

        f"{payload_hash}"

    )

    return hashlib.sha256(

        raw.encode()

    ).hexdigest()