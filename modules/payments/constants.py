from enum import Enum


class PaymentStatus(str, Enum):

    PENDING = "PENDING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"


class PaymentReferenceType(str, Enum):

    SALE = "SALE"

    RECEIVABLE = "RECEIVABLE"

    PAYABLE = "PAYABLE"

    EXPENSE = "EXPENSE"

    TRANSFER = "TRANSFER"

    RAILONE_INTENT = "RAILONE_INTENT"