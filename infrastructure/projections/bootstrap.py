from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.event_store.repository import (
    EventRepository
)

from infrastructure.projections.repository import (
    ProjectionRepository
)

from infrastructure.projections.worker import (
    ProjectionWorker
)

from modules.inventory.projector import (
    InventoryProjector
)


def run_projection_workers():

    db = SessionLocal()

    event_repo = EventRepository(
        db
    )

    projection_repo = ProjectionRepository(
        db
    )

    inventory_worker = (
        ProjectionWorker(

            event_repo=
                event_repo,

            projection_repo=
                projection_repo,

            projector=
                InventoryProjector(db)

        )
    )

    inventory_worker.run()