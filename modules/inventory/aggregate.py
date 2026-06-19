from modules.inventory.query_service import (
    get_stock
)


class InsufficientStockError(
    Exception
):
    pass


class InventoryAggregate:

    def __init__(

        self,

        branch_id: str,

        product_id: str

    ):

        self.stock = get_stock(

            branch_id,

            product_id

        )

    def validate_deduction(

        self,

        quantity: int

    ):

        if quantity > self.stock:

            raise (

                InsufficientStockError(

                    f"Available "

                    f"{self.stock}, "

                    f"Requested "

                    f"{quantity}"

                )

            )