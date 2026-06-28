from dataclasses import dataclass
from typing import Optional

from core.commands.command import Command


@dataclass
class PurchaseLineCommand:
    product_id: str
    sku: str
    quantity: int
    unit_cost: float


@dataclass
class ReceivePurchaseLineCommand:
    product_id: str
    sku: str
    quantity: int
    cost_price: float
    inventory_expected_version: int


@dataclass
class CreatePurchaseCommand(Command):
    merchant_id: str
    branch_id: str
    supplier_id: str
    items: list[PurchaseLineCommand]
    purchase_id: Optional[str] = None
    supplier_invoice_ref: Optional[str] = None
    notes: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class ReceivePurchaseCommand(Command):
    merchant_id: str
    purchase_id: str
    items: list[ReceivePurchaseLineCommand]
    expected_version: int
    received_by_user_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class CancelPurchaseCommand(Command):
    merchant_id: str
    purchase_id: str
    expected_version: int
    reason: Optional[str] = None
    idempotency_key: Optional[str] = None