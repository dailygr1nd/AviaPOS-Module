from typing import Optional

from pydantic import BaseModel, Field


class StockTransferItem(BaseModel):
    product_id: str
    sku: str

    quantity: int = Field(
        gt=0
    )


class DispatchStockTransferItem(BaseModel):
    product_id: str
    sku: str

    quantity: int = Field(
        gt=0
    )

    source_inventory_expected_version: int = Field(
        ge=0
    )


class ReceiveStockTransferItem(BaseModel):
    product_id: str
    sku: str

    quantity: int = Field(
        gt=0
    )

    cost_price: float = Field(
        ge=0
    )

    destination_inventory_expected_version: int = Field(
        ge=0
    )


class CreateStockTransferRequest(BaseModel):
    merchant_id: str
    source_branch_id: str
    destination_branch_id: str
    transfer_id: Optional[str] = None
    notes: Optional[str] = None
    items: list[StockTransferItem]


class DispatchStockTransferRequest(BaseModel):
    merchant_id: str
    transfer_id: str
    dispatched_by_user_id: Optional[str] = None
    items: list[DispatchStockTransferItem]


class ReceiveStockTransferRequest(BaseModel):
    merchant_id: str
    transfer_id: str
    received_by_user_id: Optional[str] = None
    items: list[ReceiveStockTransferItem]


class CancelTransferRequest(BaseModel):
    merchant_id: str
    transfer_id: str
    reason: Optional[str] = None


class CreateFundsMovementIntentRequest(BaseModel):
    merchant_id: str

    amount: float = Field(
        gt=0
    )

    currency: str = Field(
        min_length=3,
        max_length=3
    )

    destination_type: str
    destination_reference: str

    source_branch_id: Optional[str] = None
    destination_branch_id: Optional[str] = None
    transfer_id: Optional[str] = None
    purpose: Optional[str] = None
    rail_hint: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None


class ConfirmFundsMovementRequest(BaseModel):
    merchant_id: str
    transfer_id: str
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None
    reconciliation_state: str = "CONFIRMED"


class FailFundsMovementRequest(BaseModel):
    merchant_id: str
    transfer_id: str
    reason: Optional[str] = None
    provider_reference: Optional[str] = None
    external_reference: Optional[str] = None
    railone_intent_id: Optional[str] = None