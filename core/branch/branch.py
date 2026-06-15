from dataclasses import dataclass


@dataclass
class Branch:

    branch_id: str

    merchant_id: str

    branch_name: str

    location: str

    active: bool = True