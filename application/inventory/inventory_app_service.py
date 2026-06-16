from app_context import (

    store,

    event_bus

)

from modules.inventory.service import (

    receive_stock,

    deduct_stock
)

class InventoryApplicationService:
        def receive_stock(

        self,

        merchant_id,

        product_id,

        quantity,

        unit_cost

    ):
                previous_hash = (

            store.latest_hash(

                merchant_id

            )

        )
                event = receive_stock(

            merchant_id=
                merchant_id,

            product_id=
                product_id,

            quantity=
                quantity,

            unit_cost=
                unit_cost,

            previous_hash=
                previous_hash
        )
                store.append(
            event
        )


        def deduct_stock(

        self,

        merchant_id,

        product_id,

        quantity

    ):
                previous_hash = (

            store.latest_hash(

                merchant_id

            )

        )
                event = deduct_stock(

            merchant_id=
                merchant_id,

            product_id=
                product_id,

            quantity=
                quantity,

            previous_hash=
                previous_hash
        )
                store.append(
            event
        )