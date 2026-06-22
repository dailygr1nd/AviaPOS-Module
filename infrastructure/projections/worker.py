from infrastructure.projections.repository import (
    ProjectionRepository
)

from infrastructure.event_store.repository import (
    EventRepository
)


class ProjectionWorker:

    def __init__(

        self,

        event_repo,

        projection_repo,

        projector

    ):

        self.event_repo = event_repo

        self.projection_repo = projection_repo

        self.projector = projector

    def run(self):

        offset = (

            self.projection_repo
            .get_offset(

                self.projector
                .projection_name

            )

        )

        events = (

            self.event_repo
            .get_after_id(
                offset
            )

        )

        for event in events:

            self.projector.handle(
                event
            )

            self.projection_repo.save_offset(

                self.projector
                .projection_name,

                event.id

            )