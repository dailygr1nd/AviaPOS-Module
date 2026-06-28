from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class CreatePaymentCommand(
    Command
):

    merchant_id: str

    amount: float

    payment_method: str

    reference_type: str

    reference_id: str

    notes: Optional[str] = None

    idempotency_key: Optional[str] = None


@dataclass
class CompletePaymentCommand(
    Command
):

    merchant_id: str

    payment_id: str

    expected_version: int

    idempotency_key: Optional[str] = None


@dataclass
class FailPaymentCommand(
    Command
):

    merchant_id: str

    payment_id: str

    reason: Optional[str] = None

    expected_version: int = 1

    idempotency_key: Optional[str] = None


@dataclass
class CancelPaymentCommand(
    Command
):

    merchant_id: str

    payment_id: str

    reason: Optional[str] = None

    expected_version: int = 1

    idempotency_key: Optional[str] = None