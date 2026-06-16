from app_context import (

    store,

    event_bus

)

from modules.debts.service import (
    create_debt
)

class DebtApplicationService:

    def create_debt(

        self,

        merchant_id,

        customer_id,

        amount,

        currency,

        due_date

    ):
                previous_hash = (

            store.latest_hash(

                merchant_id

            )

        )

                event = create_debt(

            merchant_id=
                merchant_id,

            customer_id=
                customer_id,

            amount=
                amount,

            currency=
                currency,

            due_date=
                due_date,

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