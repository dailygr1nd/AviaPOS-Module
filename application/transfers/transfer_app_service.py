from app_context import (
    store,
    event_bus
)

from modules.transfers.service import (
    create_branch_transfer
)


class TransferApplicationService:

    def create_transfer(

        self,

        merchant_id: str,

        source_branch: str,

        destination_branch: str,

        amount: float,

        currency: str

    ):

        previous_hash = (

            store.latest_hash(
                merchant_id
            )

        )

        event = create_branch_transfer(

            merchant_id=
                merchant_id,

            source_branch=
                source_branch,

            destination_branch=
                destination_branch,

            amount=
                amount,

            currency=
                currency,

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