from storage.sqlite.projection_store import (
    ProjectionStore
)


class DashboardService:

    def __init__(

        self,

        store

    ):

        self.store = store

        self.projection_store = (
            ProjectionStore(
                "aviapos.db"
            )
        )

    def build(

        self,

        merchant_id: str

    ):

        cached = (

            self.projection_store.load(

                "dashboard",

                merchant_id

            )

        )

        if cached:

            return cached

        events = (

            self.store.replay_events(

                merchant_id

            )

        )

        dashboard = {

            "merchant_id":
                merchant_id,

            "event_count":
                len(events),

            "total_sales":
                0,

            "sales_count":
                0,

            "products_tracked":
                0,

            "outstanding_debt":
                0

        }

        self.projection_store.save(

            "dashboard",

            merchant_id,

            dashboard

        )

        return dashboard