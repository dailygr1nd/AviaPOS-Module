class InventoryProjection:

    def apply(
        self,
        event
    ):

        if event.event_type == "STOCK_RECEIVED":

            pass

        elif event.event_type == "STOCK_DEDUCTED":

            pass