from dataclasses import dataclass
from typing import Optional

from core.commands.command import Command


@dataclass
class StockTransferLineCommand:
    product_id: str
    sku: str
    quantity: int


@dataclass
class DispatchStockTransferLineCommand:
    product_id: str
    sku: str
    quantity: int
    source_inventory_expected_version: int


@dataclass
class ReceiveStockTransferLineCommand:
    product_id: str
    sku: str
    quantity: int
    cost_price: float
    destination_inventory_expected_version: int


@dataclass
class CreateStockTransferCommand(Command):
    merchant_id: str
    source_branch_id: str
    destination_branch_id: str
    items: list[StockTransferLineCommand]
    transfer_id: Optional[str] = None
    notes: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class DispatchStockTransferCommand(Command):
    merchant_id: str
    transfer_id: str
    items: list[DispatchStockTransferLineCommand]
    expected_version: int
    dispatched_by_user_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class ReceiveStockTransferCommand(Command):
    merchant_id: str
    transfer_id: str
    items: list[ReceiveStockTransferLineCommand]
    expected_version: int
    received_by_user_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class CancelTransferCommand(Command):
    merchant_id: str
    transfer_id: str
    expected_version: int
    reason: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class CreateFundsMovementIntentCommand(Command):
    merchant_id: str
    amount: float
    currency: str
    destination_type: str
    destination_reference: str
    source_branch_id: Optional[str] = None
    destination_branch_id: Optional[str] = None
    transfer_id: Optional[str] = None
    purpose: Optional[str] = None
    rail_hint: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class ConfirmFundsMovementCommand(Command):
    merchant_id: str
    transfer_id: str
    expected_version: int
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    reconciliation_state: str = "CONFIRMED"
    idempotency_key: Optional[str] = None


@dataclass
class FailFundsMovementCommand(Command):
    merchant_id: str
    transfer_id: str
    expected_version: int
    reason: Optional[str] = None
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    idempotency_key: Optional[str] = None