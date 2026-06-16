class SupplierProjection:

    def __init__(self):

        self.suppliers = {}

    def apply(self, event):

        event_type = event["event_type"]

        payload = event["payload"]

        if event_type == "SUPPLIER_CREATED":

            supplier_id = payload["supplier_id"]

            self.suppliers[supplier_id] = {

                "name": payload["name"],

                "balance": 0
            }

        elif event_type == "SUPPLIER_DEBT_CREATED":

            supplier_id = payload["supplier_id"]

            if supplier_id in self.suppliers:

                self.suppliers[supplier_id][

                    "balance"

                ] += payload["amount"]

        elif event_type == "SUPPLIER_PAYMENT_MADE":

            supplier_id = payload["supplier_id"]

            if supplier_id in self.suppliers:

                self.suppliers[supplier_id][

                    "balance"

                ] -= payload["amount"]

    def replay(self, events):

        for event in events:

            self.apply(event)