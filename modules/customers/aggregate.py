class CustomerValidationError(
    Exception
):
    pass


class CustomerAggregate:

    @staticmethod
    def validate_create(
        name: str
    ):

        if not name:

            raise (
                CustomerValidationError(
                    "Customer name required"
                )
            )