from app_context import (

    store,

    event_bus

)

from modules.sales.service import (
    create_sale
)

class SalesApplicationService:

    def create_sale(

        self,

        merchant_id,

        amount,

        currency,

        items,

        payment_method

    ):
                previous_hash = (

            store.latest_hash(

                merchant_id

            )

        )
                event = create_sale(

            merchant_id=
                merchant_id,

            amount=
                amount,

            currency=
                currency,

            items=
                items,

            payment_method=
                payment_method,

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