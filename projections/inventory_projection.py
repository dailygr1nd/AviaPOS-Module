class InventoryProjection:

    def __init__(self):

        self.stock = {}

    def apply(

        self,

        event

    ):

        event_type = (
            event["event_type"]
        )

        payload = (
            event["payload"]
        )

        if (

            event_type ==
            "INVENTORY_RECEIVED"

        ):

            product_id = (

                payload["product_id"]

            )

            quantity = (

                payload["quantity"]

            )

            self.stock[
                product_id
            ] = (

                self.stock.get(
                    product_id,
                    0
                )

                +

                quantity
            )

        elif (

            event_type ==
            "SALE_CREATED"

        ):

            product_id = (

                payload["product_id"]

            )

            quantity = (

                payload["quantity"]

            )

            self.stock[
                product_id
            ] = (

                self.stock.get(
                    product_id,
                    0
                )

                -

                quantity
            )

    def quantity(

        self,

        product_id: str

    ):

        return self.stock.get(

            product_id,

            0

        )