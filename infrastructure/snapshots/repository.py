from sqlalchemy.orm import Session

from infrastructure.snapshots.models import (
    SnapshotModel
)


class SnapshotRepository:

    def __init__(self, db: Session):

        self.db = db

    def save(

        self,

        aggregate_id: str,

        aggregate_type: str,

        version: int,

        state: dict

    ):

        snapshot = SnapshotModel(

            aggregate_id=aggregate_id,

            aggregate_type=aggregate_type,

            version=version,

            state=state

        )

        self.db.add(snapshot)

        self.db.commit()

        return snapshot

    def get_latest(

        self,

        aggregate_id: str

    ):

        return (

            self.db.query(SnapshotModel)

            .filter(
                SnapshotModel.aggregate_id
                == aggregate_id
            )

            .order_by(
                SnapshotModel.version.desc()
            )

            .first()

        )