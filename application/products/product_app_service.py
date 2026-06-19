from app_context import (
    store,
    event_bus
)

from modules.products.service import (
    create_product
)


class ProductApplicationService:

    def create_product(

        self,

        merchant_id: str,

        sku: str,

        name: str,

        price: float

    ):

        previous_hash = (

            store.latest_hash(
                merchant_id
            )

        )

        event = create_product(

            merchant_id=
                merchant_id,

            sku=
                sku,

            name=
                name,

            price=
                price,

            previous_hash=
                previous_hash

        )

        store.append(
            event
        )

        event_bus.publish(
            event
        )

        return event