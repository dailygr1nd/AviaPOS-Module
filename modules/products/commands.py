from dataclasses import dataclass

from typing import Optional

from core.commands.command import (
    Command
)


@dataclass
class CreateProductCommand(
    Command
):

    merchant_id: str

    sku: str

    name: str

    selling_price: float

    cost_price: float

    product_id: Optional[str] = None

    category: Optional[str] = None

    barcode: Optional[str] = None

    idempotency_key: Optional[str] = None


@dataclass
class UpdateProductCommand(
    Command
):

    merchant_id: str

    product_id: str

    expected_version: int

    sku: Optional[str] = None

    name: Optional[str] = None

    selling_price: Optional[float] = None

    cost_price: Optional[float] = None

    category: Optional[str] = None

    barcode: Optional[str] = None

    idempotency_key: Optional[str] = None


@dataclass
class DeactivateProductCommand(
    Command
):

    merchant_id: str

    product_id: str

    expected_version: int

    reason: Optional[str] = None

    idempotency_key: Optional[str] = None