from projections.dashboard_projection import (
    DashboardProjection
)

from storage.sqlite.projection_store import (
    ProjectionStore
)

from app_context import (
    store
)

projection_store = (
    ProjectionStore(
        "aviapos.db"
    )
)

def rebuild_dashboard(

    merchant_id

):
        events = (

        store.replay_events(

            merchant_id

        )

    )
        dashboard = (

        DashboardProjection()

        .build(events)

    )
        projection_store.save(

        "dashboard",

        merchant_id,

        dashboard

    )
        
def handle_sale_created(
    event
):

    rebuild_dashboard(
        event.merchant_id
    )


def handle_debt_created(
    event
):

    rebuild_dashboard(
        event.merchant_id
    )


def handle_stock_received(
    event
):

    rebuild_dashboard(
        event.merchant_id
    )


def handle_stock_deducted(
    event
):

    rebuild_dashboard(
        event.merchant_id
    )