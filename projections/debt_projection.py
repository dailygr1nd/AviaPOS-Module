class DebtProjection:

    def __init__(self):

        self.balances = {}

    def apply(self, event):

        payload = event["payload"]

        customer_id = payload.get(

            "customer_id"
        )

        if not customer_id:

            return

        if event["event_type"] == "DEBT_CREATED":

            self.balances[customer_id] = (

                self.balances.get(

                    customer_id,

                    0

                )

                +

                payload.get(

                    "amount",

                    0

                )

            )

        elif event["event_type"] == "DEBT_SETTLED":

            self.balances[customer_id] = (

                self.balances.get(

                    customer_id,

                    0

                )

                -

                payload.get(

                    "amount",

                    0

                )

            )

    def replay(self, events):

        for event in events:

            self.apply(event)