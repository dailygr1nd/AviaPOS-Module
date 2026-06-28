from enum import Enum


class Role(str, Enum):

    OWNER = "OWNER"

    MANAGER = "MANAGER"

    CASHIER = "CASHIER"

    INVENTORY_CLERK = "INVENTORY_CLERK"

    ACCOUNTANT = "ACCOUNTANT"


ROLE_HIERARCHY = {

    Role.OWNER: 100,

    Role.MANAGER: 80,

    Role.ACCOUNTANT: 60,

    Role.INVENTORY_CLERK: 50,

    Role.CASHIER: 40

}


def role_level(
    role: str
) -> int:

    try:

        return ROLE_HIERARCHY[
            Role(role)
        ]

    except Exception:

        return 0


def has_minimum_role(

    user_role: str,

    required_role: Role

) -> bool:

    return role_level(
        user_role
    ) >= role_level(
        required_role.value
    )