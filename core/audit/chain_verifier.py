from core.events.hash import (
    calculate_event_hash,
    calculate_payload_hash
)


class ChainVerifier:

    @staticmethod
    def _value(
        event,
        key: str,
        default=None
    ):

        if isinstance(
            event,
            dict
        ):

            return event.get(
                key,
                default
            )

        return getattr(
            event,
            key,
            default
        )

    @classmethod
    def _verify_single_event_hash(
        cls,
        event
    ):

        payload = cls._value(
            event,
            "payload",
            {}
        )

        event_type = cls._value(
            event,
            "event_type"
        )

        merchant_id = cls._value(
            event,
            "merchant_id"
        )

        previous_hash = cls._value(
            event,
            "previous_hash"
        )

        current_hash = (

            cls._value(
                event,
                "current_hash",
                None
            )

            or

            cls._value(
                event,
                "event_hash",
                None
            )

        )

        payload_hash = calculate_payload_hash(
            payload
        )

        expected_hash = calculate_event_hash(

            event_type,

            merchant_id,

            payload_hash,

            previous_hash

        )

        return {

            "valid":
                expected_hash == current_hash,

            "expected_hash":
                expected_hash,

            "actual_hash":
                current_hash,

            "payload_hash":
                payload_hash

        }

    @classmethod
    def verify_events(

        cls,

        events,

        strict_previous_hash: bool = True

    ):

        issues = []

        previous_hash = "GENESIS"

        checked = 0

        for event in events:

            checked += 1

            event_id = cls._value(
                event,
                "event_id"
            )

            db_id = cls._value(
                event,
                "id"
            )

            stored_previous_hash = cls._value(
                event,
                "previous_hash"
            )

            current_hash = (

                cls._value(
                    event,
                    "current_hash",
                    None
                )

                or

                cls._value(
                    event,
                    "event_hash",
                    None
                )

            )

            hash_result = cls._verify_single_event_hash(
                event
            )

            if not hash_result[
                "valid"
            ]:

                issues.append(

                    {

                        "type":
                            "INVALID_EVENT_HASH",

                        "db_id":
                            db_id,

                        "event_id":
                            event_id,

                        "expected_hash":
                            hash_result[
                                "expected_hash"
                            ],

                        "actual_hash":
                            hash_result[
                                "actual_hash"
                            ]

                    }

                )

            if strict_previous_hash:

                if stored_previous_hash != previous_hash:

                    issues.append(

                        {

                            "type":
                                "BROKEN_PREVIOUS_HASH_LINK",

                            "db_id":
                                db_id,

                            "event_id":
                                event_id,

                            "expected_previous_hash":
                                previous_hash,

                            "actual_previous_hash":
                                stored_previous_hash

                        }

                    )

                previous_hash = current_hash

        return {

            "valid":
                len(
                    issues
                ) == 0,

            "events_checked":
                checked,

            "issues":
                issues

        }

    @classmethod
    def verify_merchant_chain(
        cls,
        events
    ):

        return cls.verify_events(

            events,

            strict_previous_hash=True

        )

    @classmethod
    def verify_event_integrity(
        cls,
        events
    ):

        return cls.verify_events(

            events,

            strict_previous_hash=False

        )