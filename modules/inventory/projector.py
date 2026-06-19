from core.events.types import EventType

from modules.inventory.projection import (
    inventory
)


class InventoryProjector:

    @staticmethod
    def reset():

        inventory.clear()

    @staticmethod
    def apply(event):

        payload = event["payload"]

        event_type = (
            event["event_type"]
        )

        if "branch_id" not in payload:

            return

        key = (

            payload["branch_id"],

            payload["product_id"]

        )

        if key not in inventory:

            inventory[key] = 0

        if (

            event_type ==

            EventType
            .INVENTORY_RECEIVED
            .value

        ):

            inventory[key] += (
                payload["quantity"]
            )

        elif (

            event_type ==

            EventType
            .INVENTORY_DEDUCTED
            .value

        ):

            inventory[key] -= (
                payload["quantity"]
            )

        elif (

            event_type ==

            EventType
            .INVENTORY_ADJUSTED
            .value

        ):

            inventory[key] += (
                payload["adjustment"]
            )