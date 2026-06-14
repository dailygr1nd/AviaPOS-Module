import json

from collections import defaultdict


class DebtProjection:

    def __init__(self):

        self.balances = defaultdict(
            float
        )

    def replay(

        self,

        events

    ):

        self.balances.clear()

        for event in events:

            payload = json.loads(
                event["payload"]
            )

            if (
                event["event_type"]
                ==
                "DEBT_CREATED"
            ):

                self.balances[

                    payload[
                        "customer_id"
                    ]

                ] += payload[
                    "amount"
                ]

            elif (

                event["event_type"]

                ==
                "DEBT_SETTLED"

            ):

                self.balances[

                    payload[
                        "customer_id"
                    ]

                ] -= payload[
                    "amount"
                ]