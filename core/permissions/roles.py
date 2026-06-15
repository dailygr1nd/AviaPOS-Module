from enum import Enum


class Role(str, Enum):

    OWNER = "OWNER"

    MANAGER = "MANAGER"

    CASHIER = "CASHIER"

    INVENTORY_CLERK = "INVENTORY_CLERK"