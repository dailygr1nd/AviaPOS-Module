from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class SaleLineCommand:

    product_id: str

    sku: str

    quantity: int

    unit_price: float

    inventory_expected_version: int


@dataclass
class CreateSaleCommand(
    Command
):

    merchant_id: str

    branch_id: str

    items: list[SaleLineCommand]

    payment_method: str

    customer_id: Optional[str] = None

    idempotency_key: Optional[str] = None