from sqlalchemy.orm import Session

from infrastructure.projections.checkpoints import (
    ProjectionCheckpoint
)


class ProjectionRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def get_offset(
        self,
        projection_name: str
    ):

        checkpoint = (

            self.db.query(
                ProjectionCheckpoint
            )

            .filter(
                ProjectionCheckpoint.projection_name
                == projection_name
            )

            .first()

        )

        if not checkpoint:
            return 0

        return checkpoint.last_event_id

    def save_offset(

        self,

        projection_name: str,

        event_id: int

    ):

        checkpoint = (

            self.db.query(
                ProjectionCheckpoint
            )

            .filter(
                ProjectionCheckpoint.projection_name
                == projection_name
            )

            .first()

        )

        if checkpoint:

            checkpoint.last_event_id = event_id

        else:

            checkpoint = ProjectionCheckpoint(

                projection_name=
                    projection_name,

                last_event_id=
                    event_id

            )

            self.db.add(
                checkpoint
            )

        self.db.commit()