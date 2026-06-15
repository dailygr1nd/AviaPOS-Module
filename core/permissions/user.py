from dataclasses import dataclass

from core.permissions.roles import (
    Role
)


@dataclass
class User:

    user_id: str

    merchant_id: str

    username: str

    role: Role