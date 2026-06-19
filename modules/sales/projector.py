from core.events.types import EventType

from modules.sales.projection import sales


class SalesProjector:

    @staticmethod
    def reset():

        sales.clear()

    @staticmethod
    def apply(event):

        event_type = event["event_type"]
        payload = event["payload"]

        if event_type == EventType.SALE_CREATED.value:

            sales[payload["sale_id"]] = {

                "sale_id": payload["sale_id"],
                "customer_id": payload.get("customer_id"),
                "lines": [],
                "total": 0,
                "status": "OPEN"

            }

        elif event_type == EventType.SALE_LINE_ADDED.value:

            sale = sales[payload["sale_id"]]

            sale["lines"].append(payload)
            sale["total"] += payload["line_total"]

        elif event_type == EventType.SALE_COMPLETED.value:

            sales[payload["sale_id"]]["status"] = "COMPLETED"

        elif event_type == EventType.SALE_CANCELLED.value:

            sales[payload["sale_id"]]["status"] = "CANCELLED"