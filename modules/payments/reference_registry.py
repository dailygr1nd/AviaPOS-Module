from modules.payments.constants import (
    PaymentReferenceType
)


class PaymentReferenceRegistry:

    SUPPORTED_TYPES = {

        PaymentReferenceType.SALE,

        PaymentReferenceType.RECEIVABLE,

        PaymentReferenceType.PAYABLE,

        PaymentReferenceType.EXPENSE,

        PaymentReferenceType.TRANSFER,

        PaymentReferenceType.RAILONE_INTENT

    }

    @classmethod
    def validate(

        cls,

        reference_type

    ):

        if reference_type not in cls.SUPPORTED_TYPES:

            raise ValueError(

                f"Unsupported reference type: "

                f"{reference_type}"

            )