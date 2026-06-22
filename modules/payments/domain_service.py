from modules.payments.policy_engine import (
    PaymentPolicyEngine
)

from modules.payments.reference_registry import (
    PaymentReferenceRegistry
)


class PaymentDomainService:

    @staticmethod
    def validate_creation(

        reference_type

    ):

        PaymentReferenceRegistry.validate(

            reference_type
        )

    @staticmethod
    def validate_status_change(

        current_status,

        new_status

    ):

        PaymentPolicyEngine.validate_transition(

            current_status,

            new_status

        )