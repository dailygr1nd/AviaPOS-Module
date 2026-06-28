from typing import Optional

from pydantic import BaseModel, Field


class PurchaseItem(BaseModel):
    product_id: str
    sku: str

    quantity: int = Field(
        gt=0
    )

    unit_cost: float = Field(
        ge=0
    )


class ReceivePurchaseItem(BaseModel):
    product_id: str
    sku: str

    quantity: int = Field(
        gt=0
    )

    cost_price: float = Field(
        ge=0
    )

    inventory_expected_version: int = Field(
        ge=0
    )


class CreatePurchaseRequest(BaseModel):
    merchant_id: str
    branch_id: str
    supplier_id: str
    purchase_id: Optional[str] = None
    supplier_invoice_ref: Optional[str] = None
    notes: Optional[str] = None
    items: list[PurchaseItem]


class ReceivePurchaseRequest(BaseModel):
    merchant_id: str
    purchase_id: str
    received_by_user_id: Optional[str] = None
    items: list[ReceivePurchaseItem]


class CancelPurchaseRequest(BaseModel):
    merchant_id: str
    purchase_id: str
    reason: Optional[str] = None