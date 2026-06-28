from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class ReceiveInventoryCommand(
    Command
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    quantity: int

    cost_price: float

    expected_version: int

    idempotency_key: Optional[str] = None


@dataclass
class DeductInventoryCommand(
    Command
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    quantity: int

    reason: str

    expected_version: int

    idempotency_key: Optional[str] = None


@dataclass
class AdjustInventoryCommand(
    Command
):

    merchant_id: str

    branch_id: str

    product_id: str

    sku: str

    adjustment: int

    reason: str

    expected_version: int

    idempotency_key: Optional[str] = None