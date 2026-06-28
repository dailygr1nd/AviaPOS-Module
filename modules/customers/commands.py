from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class CreateCustomerCommand(
    Command
):

    merchant_id: str

    name: str

    customer_id: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    address: Optional[str] = None

    credit_limit: float = 0

    idempotency_key: Optional[str] = None


@dataclass
class UpdateCustomerCommand(
    Command
):

    merchant_id: str

    customer_id: str

    expected_version: int

    name: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    address: Optional[str] = None

    credit_limit: Optional[float] = None

    idempotency_key: Optional[str] = None


@dataclass
class DeactivateCustomerCommand(
    Command
):

    merchant_id: str

    customer_id: str

    expected_version: int

    reason: Optional[str] = None

    idempotency_key: Optional[str] = None