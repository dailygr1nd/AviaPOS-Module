from dataclasses import dataclass
from typing import Optional

from core.commands.command import Command


@dataclass
class CreateSupplierCommand(Command):
    merchant_id: str
    name: str
    supplier_id: Optional[str] = None
    supplier_code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class UpdateSupplierCommand(Command):
    merchant_id: str
    supplier_id: str
    expected_version: int
    name: Optional[str] = None
    supplier_code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class DeactivateSupplierCommand(Command):
    merchant_id: str
    supplier_id: str
    expected_version: int
    reason: Optional[str] = None
    idempotency_key: Optional[str] = None