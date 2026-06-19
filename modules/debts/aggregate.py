class DebtError(
    Exception
):
    pass


class DebtAggregate:

    @staticmethod
    def validate_amount(
        amount: float
    ):

        if amount <= 0:

            raise DebtError(
                "Debt amount must be positive"
            )