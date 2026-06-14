import json


class ProductProjection:

    def __init__(self):

        self.products = {}

    def replay(

        self,

        events

    ):

        self.products.clear()

        for event in events:

            payload = json.loads(
                event["payload"]
            )

            if (

                event["event_type"]

                ==

                "PRODUCT_CREATED"

            ):

                self.products[
                    payload["sku"]
                ] = payload

            elif (

                event["event_type"]

                ==

                "PRODUCT_UPDATED"

            ):

                sku = payload["sku"]

                if sku in self.products:

                    self.products[sku].update(
                        payload
                    )

    def get_product(

        self,

        sku: str

    ):

        return self.products.get(
            sku
        )

    def all_products(self):

        return list(
            self.products.values()
        )