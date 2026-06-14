import hashlib

def calculate_event_hash(

    event_type,

    merchant_id,

    timestamp,

    previous_hash,

    payload_hash

):

    body = (

        event_type +

        merchant_id +

        timestamp +

        previous_hash +

        payload_hash

    )

    return hashlib.sha256(

        body.encode()

    ).hexdigest()