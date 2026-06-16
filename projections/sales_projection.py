class SalesProjection:

    def __init__(self):

        self.total_sales = 0

        self.sale_count = 0

    def apply(self, event):

        if event["event_type"] != "SALE_CREATED":

            return

        amount = event["payload"].get(

            "amount",

            0

        )

        self.total_sales += amount

        self.sale_count += 1

    def replay(self, events):

        for event in events:

            self.apply(event)

    def total(self):

        return self.total_sales

    def count(self):

        return self.sale_count