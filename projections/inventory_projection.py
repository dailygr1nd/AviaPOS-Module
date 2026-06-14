from collections import defaultdict


class InventoryProjection:

    def __init__(self):

        self.stock = defaultdict(
            int
        )

    def replay(

        self,

        events

    ):

        self.stock.clear()

        for event in events:

            payload = eval(
                event["payload"]
            )

            if (
                event["event_type"]
                ==
                "STOCK_RECEIVED"
            ):

                self.stock[
                    payload["sku"]
                ] += payload[
                    "quantity"
                ]

            elif (
                event["event_type"]
                ==
                "STOCK_DEDUCTED"
            ):

                self.stock[
                    payload["sku"]
                ] -= payload[
                    "quantity"
                ]

    def get_stock(

        self,

        sku

    ):

        return self.stock.get(
            sku,
            0
        )