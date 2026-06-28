from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class CreateExpenseCommand(
    Command
):

    merchant_id: str

    branch_id: str

    category: str

    description: str

    amount: float

    reference: Optional[str] = None

    idempotency_key: Optional[str] = None


@dataclass
class ApproveExpenseCommand(
    Command
):

    merchant_id: str

    expense_id: str

    idempotency_key: Optional[str] = None


@dataclass
class PayExpenseCommand(
    Command
):

    merchant_id: str

    expense_id: str

    payment_method: str

    idempotency_key: Optional[str] = None