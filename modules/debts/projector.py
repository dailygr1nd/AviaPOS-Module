from core.events.types import EventType

from modules.debts.projection import debts


class DebtProjector:

    @staticmethod
    def reset():

        debts.clear()

    @staticmethod
    def apply(event):

        event_type = event["event_type"]
        payload = event["payload"]

        # CREATE DEBT
        if event_type == EventType.DEBT_CREATED.value:

            debts[payload["debt_id"]] = {

                "debt_id": payload["debt_id"],
                "customer_id": payload["customer_id"],
                "sale_id": payload["sale_id"],
                "original_amount": payload["amount"],
                "balance": payload["amount"],
                "status": "OPEN"

            }

        # PAYMENT
        elif event_type == EventType.DEBT_PAYMENT_RECEIVED.value:

            debt = debts.get(payload["debt_id"])

            if not debt:
                return

            debt["balance"] -= payload["amount"]

            if debt["balance"] <= 0:

                debt["status"] = "SETTLED"

        # SETTLED EVENT (optional explicit)
        elif event_type == EventType.DEBT_SETTLED.value:

            debt = debts.get(payload["debt_id"])

            if debt:
                debt["status"] = "SETTLED"