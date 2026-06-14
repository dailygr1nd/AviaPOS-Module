import json


class SalesProjection:

    def __init__(self):

        self.sales = []

        self.total_sales = 0

    def replay(

        self,

        events

    ):

        self.sales.clear()

        self.total_sales = 0

        for event in events:

            if (

                event["event_type"]

                !=

                "SALE_CREATED"

            ):

                continue

            payload = json.loads(
                event["payload"]
            )

            self.sales.append(
                payload
            )

            self.total_sales += (
                payload["amount"]
            )

    def total(self):

        return self.total_sales

    def count(self):

        return len(
            self.sales
        )