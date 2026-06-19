class SalesProjection:

    def __init__(self):

        self.total_sales = 0

        self.total_transactions = 0

    def apply(

        self,

        event

    ):

        if (

            event["event_type"]

            !=

            "SALE_CREATED"

        ):

            return

        payload = (
            event["payload"]
        )

        self.total_sales += (

            payload["amount"]

        )

        self.total_transactions += 1

    def summary(self):

        return {

            "sales":

                self.total_sales,

            "transactions":

                self.total_transactions

        }