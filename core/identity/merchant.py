from dataclasses import dataclass


@dataclass
class Merchant:

    merchant_id: str

    merchant_name: str

    owner_name: str

    phone: str

    email: str | None = None

    active: bool = True