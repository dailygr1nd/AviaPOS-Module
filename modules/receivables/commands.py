from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class CreateReceivableCommand(
    Command
):

    merchant_id: str

    branch_id: str

    customer_id: str

    sale_id: str

    amount: float

    idempotency_key: Optional[str] = None


@dataclass
class RecordReceivablePaymentCommand(
    Command
):

    merchant_id: str

    receivable_id: str

    amount: float

    payment_method: str

    expected_version: int

    idempotency_key: Optional[str] = None