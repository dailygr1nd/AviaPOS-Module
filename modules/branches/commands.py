from dataclasses import dataclass
from typing import Optional

from core.commands.command import Command


@dataclass
class CreateBranchCommand(Command):
    merchant_id: str
    name: str
    location: str
    branch_id: Optional[str] = None
    branch_code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    manager_user_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class UpdateBranchCommand(Command):
    merchant_id: str
    branch_id: str
    expected_version: int
    name: Optional[str] = None
    location: Optional[str] = None
    branch_code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    manager_user_id: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class DeactivateBranchCommand(Command):
    merchant_id: str
    branch_id: str
    expected_version: int
    reason: Optional[str] = None
    idempotency_key: Optional[str] = None