from core.events.types import EventType

from modules.customers.projection import customers


class CustomerProjector:

    @staticmethod
    def reset():

        customers.clear()

    @staticmethod
    def apply(event):

        event_type = event["event_type"]
        payload = event["payload"]

        if event_type == EventType.CUSTOMER_CREATED.value:

            customers[payload["customer_id"]] = {

                "customer_id": payload["customer_id"],
                "name": payload["name"],
                "phone": payload.get("phone", "")

            }

        elif event_type == EventType.CUSTOMER_UPDATED.value:

            customer = customers.get(payload["customer_id"])

            if customer:

                customer.update(payload)