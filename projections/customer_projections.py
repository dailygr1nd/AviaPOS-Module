import json


class CustomerProjection:

    def __init__(self):

        self.customers = {}

    def replay(

        self,

        events

    ):

        self.customers.clear()

        for event in events:

            payload = json.loads(
                event["payload"]
            )

            if (
                event["event_type"]
                ==
                "CUSTOMER_CREATED"
            ):

                self.customers[

                    payload[
                        "customer_id"
                    ]

                ] = payload