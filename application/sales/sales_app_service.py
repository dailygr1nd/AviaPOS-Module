from app_context import (
    store,
    event_bus
)

from modules.sales.service import (
    create_sale
)

from core.models.merchant_aggregate import (
    MerchantAggregate
)


class SalesApplicationService:

    def __init__(self):

        self.event_store = store

        self.event_bus = event_bus

    def create_sale(

        self,

        merchant_id: str,

        product_id: str,

        quantity: int,

        amount: float,

        currency: str

    ):

        events = self.event_store.load_events(

            merchant_id

        )

        aggregate = MerchantAggregate()

        aggregate.replay(

            events

        )

        if not aggregate.product_exists(

            product_id

        ):

            raise ValueError(

                f"Product does not exist: {product_id}"

            )

        available_stock = (

            aggregate.stock_available(

                product_id

            )

        )

        if quantity > available_stock:

            raise ValueError(

                f"Insufficient stock. Available={available_stock}"
            )

        previous_hash = (

            self.event_store.latest_hash(

                merchant_id

            )

        )

        event = create_sale(

            merchant_id=merchant_id,

            product_id=product_id,

            quantity=quantity,

            amount=amount,

            currency=currency,

            previous_hash=previous_hash

        )

        self.event_store.append(

            event

        )

        self.event_bus.publish(

            event
        )

        return {

            "success": True,

            "event_id": event.event_id,

            "event_type": event.event_type,

            "remaining_stock":

                available_stock - quantity

        }