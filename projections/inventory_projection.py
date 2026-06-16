class InventoryProjection:

    def __init__(self):

        self.stock = {}

    def apply(self, event):

        event_type = event["event_type"]

        payload = event["payload"]

        product_id = payload.get(

            "product_id"
        )

        if not product_id:

            return

        if event_type == "STOCK_RECEIVED":

            self.stock[product_id] = (

                self.stock.get(

                    product_id,

                    0

                )

                +

                payload.get(

                    "quantity",

                    0

                )

            )

        elif event_type == "STOCK_DEDUCTED":

            self.stock[product_id] = (

                self.stock.get(

                    product_id,

                    0

                )

                -

                payload.get(

                    "quantity",

                    0

                )

            )

    def replay(self, events):

        for event in events:

            self.apply(event)

    def get_stock(

        self,

        product_id

    ):

        return self.stock.get(

            product_id,

            0

        )