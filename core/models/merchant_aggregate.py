class MerchantAggregate:

    def __init__(self):

        self.inventory = {}

        self.products = {}

        self.branches = {}

    def apply(self, event):

        event_type = event["event_type"]

        payload = event["payload"]

        if event_type == "PRODUCT_CREATED":

            self.products[

                payload["product_id"]

            ] = payload

        elif event_type == "INVENTORY_RECEIVED":

            product_id = payload["product_id"]

            quantity = payload["quantity"]

            self.inventory[product_id] = (

                self.inventory.get(

                    product_id,

                    0

                )

                +

                quantity

            )

        elif event_type == "SALE_CREATED":

            product_id = payload["product_id"]

            quantity = payload["quantity"]

            self.inventory[product_id] = (

                self.inventory.get(

                    product_id,

                    0

                )

                -

                quantity

            )

        elif event_type == "BRANCH_CREATED":

            self.branches[

                payload["branch_id"]

            ] = payload

    def replay(

        self,

        events

    ):

        for event in events:

            self.apply(event)

    def stock_available(

        self,

        product_id: str

    ) -> int:

        return self.inventory.get(

            product_id,

            0

        )

    def product_exists(

        self,

        product_id: str

    ) -> bool:

        return product_id in self.products