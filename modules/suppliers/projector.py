from core.events.types import (
    EventType
)

from modules.suppliers.projection import (
    suppliers
)


class SupplierProjector:

    @staticmethod
    def reset():

        suppliers.clear()

    @staticmethod
    def apply(event):

        if (

            event["event_type"]

            !=

            EventType
            .SUPPLIER_CREATED
            .value

        ):

            return

        payload = event[
            "payload"
        ]

        suppliers[
            payload[
                "supplier_id"
            ]
        ] = payload