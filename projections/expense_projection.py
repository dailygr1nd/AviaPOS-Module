class ExpenseProjection:

    def __init__(self):

        self.total_expenses = 0

    def apply(

        self,

        event

    ):

        if (

            event["event_type"]

            !=

            "EXPENSE_RECORDED"

        ):

            return

        self.total_expenses += (

            event["payload"]["amount"]

        )

    def total(self):

        return self.total_expenses