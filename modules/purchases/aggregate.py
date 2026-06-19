from dataclasses import dataclass


@dataclass
class PurchaseLine:

    product_id: str

    sku: str

    quantity: int

    cost_price: float

    total_cost: float


class PurchaseAggregate:

    def __init__(self):

        self.lines = []

        self.total = 0

    def add_line(

        self,

        product_id: str,

        sku: str,

        quantity: int,

        cost_price: float

    ):

        total_cost = (
            quantity *
            cost_price
        )

        line = PurchaseLine(

            product_id=
                product_id,

            sku=
                sku,

            quantity=
                quantity,

            cost_price=
                cost_price,

            total_cost=
                total_cost

        )

        self.lines.append(
            line
        )

        self.total += (
            total_cost
        )

        return line