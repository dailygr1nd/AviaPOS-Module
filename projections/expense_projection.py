class ExpenseProjection:

    def __init__(self):

        self.total_expenses = 0

    def apply(self, event):

        if event["event_type"] != "EXPENSE_CREATED":

            return

        self.total_expenses += (

            event["payload"].get(

                "amount",

                0

            )

        )

    def replay(self, events):

        for event in events:

            self.apply(event)