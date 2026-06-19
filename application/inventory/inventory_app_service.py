from app_context import (
    store,
    event_bus
)

from modules.inventory.service import (
    receive_stock
)


class InventoryApplicationService:

    def create_stock_receipt(

        self,

        merchant_id: str,

        product_id: str,

        sku: str,

        quantity: int,

        cost_price: float

    ):

        previous_hash = (

            store.latest_hash(
                merchant_id
            )

        )

        event = receive_stock(

            merchant_id=merchant_id,

            product_id=product_id,

            sku=sku,

            quantity=quantity,

            cost_price=cost_price,

            previous_hash=previous_hash

        )

        store.append(
            event
        )

        event_bus.publish(
            event
        )

        return event