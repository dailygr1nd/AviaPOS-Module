class ProductProjection:

    def __init__(self):

        self.products = {}

    def apply(

        self,

        event

    ):

        if event["event_type"] != "PRODUCT_CREATED":

            return

        payload = event["payload"]

        self.products[

            payload["product_id"]

        ] = payload

    def rebuild(

        self,

        events

    ):

        self.products = {}

        for event in events:

            self.apply(event)

    def list_products(self):

        return list(

            self.products.values()

        )

    def get_product(

        self,

        product_id

    ):

        return self.products.get(

            product_id

        )