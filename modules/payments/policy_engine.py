from modules.payments.constants import (
    PaymentStatus
)


class PaymentPolicyEngine:

    VALID_TRANSITIONS = {

        PaymentStatus.PENDING: [

            PaymentStatus.COMPLETED,

            PaymentStatus.FAILED,

            PaymentStatus.CANCELLED

        ],

        PaymentStatus.COMPLETED: [],

        PaymentStatus.FAILED: [],

        PaymentStatus.CANCELLED: []

    }

    @classmethod
    def can_transition(

        cls,

        current_status,

        new_status

    ):

        return (

            new_status

            in

            cls.VALID_TRANSITIONS.get(

                current_status,

                []

            )

        )

    @classmethod
    def validate_transition(

        cls,

        current_status,

        new_status

    ):

        if not cls.can_transition(

            current_status,

            new_status

        ):

            raise ValueError(

                f"Invalid payment transition: "

                f"{current_status} -> {new_status}"

            )