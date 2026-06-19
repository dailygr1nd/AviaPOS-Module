from fastapi import APIRouter

from app_context import (
    store
)

from projections.dashboard_projection import (
    DashboardProjection
)

router = APIRouter()


@router.get("/")

def dashboard(

    merchant_id: str

):

    events = (

        store.load_events(
            merchant_id
        )

    )

    projection = (

        DashboardProjection()
    )

    data = projection.build(
        events
    )

    return data