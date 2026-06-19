class DebtProjection:

    def __init__(self):

        self.total_debt = 0

    def apply(

        self,

        event

    ):

        event_type = (

            event["event_type"]

        )

        payload = (

            event["payload"]

        )

        if (

            event_type

            ==

            "DEBT_CREATED"

        ):

            self.total_debt += (

                payload["amount"]

            )

        elif (

            event_type

            ==

            "DEBT_SETTLED"

        ):

            self.total_debt -= (

                payload["amount"]

            )

    def outstanding(self):

        return self.total_debt