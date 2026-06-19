class ProductValidationError(
    Exception
):
    pass


class ProductAggregate:

    @staticmethod
    def validate_create(
        name: str,
        sku: str
    ):

        if not name:

            raise ProductValidationError(
                "Product name required"
            )

        if not sku:

            raise ProductValidationError(
                "SKU required"
            )