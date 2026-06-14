from core.events.event_hash import (
    calculate_event_hash
)

def verify_chain(events):

    previous_hash = (
        "GENESIS"
    )

    for event in events:

        expected = (

            calculate_event_hash(

                event["event_type"],

                event["merchant_id"],

                event["timestamp"],

                previous_hash,

                event["payload_hash"]

            )

        )

        if (

            expected

            !=

            event["event_hash"]

        ):

            return False

        previous_hash = (
            event["event_hash"]
        )

    return True