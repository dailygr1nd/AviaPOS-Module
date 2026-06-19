from dataclasses import dataclass


@dataclass
class SaleLine:

    product_id: str

    sku: str

    quantity: int

    unit_price: float

    line_total: float


class SaleAggregate:

    def __init__(self):

        self.lines = []

        self.total = 0

    def add_line(

        self,

        product_id: str,

        sku: str,

        quantity: int,

        unit_price: float

    ):

        if quantity <= 0:

            raise ValueError(
                "Quantity must be positive"
            )

        line_total = (
            quantity *
            unit_price
        )

        line = SaleLine(

            product_id=product_id,

            sku=sku,

            quantity=quantity,

            unit_price=unit_price,

            line_total=line_total

        )

        self.lines.append(
            line
        )

        self.total += (
            line_total
        )

        return line