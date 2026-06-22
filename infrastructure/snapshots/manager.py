from infrastructure.snapshots.service import (
    should_snapshot
)

from infrastructure.snapshots.repository import (
    SnapshotRepository
)


class SnapshotManager:

    def __init__(

        self,

        snapshot_repo: SnapshotRepository

    ):

        self.snapshot_repo = snapshot_repo

    def process(

        self,

        aggregate,

        version: int,

        aggregate_type: str

    ):

        if not should_snapshot(
            version
        ):

            return

        self.snapshot_repo.save(

            aggregate_id=
                aggregate.id,

            aggregate_type=
                aggregate_type,

            version=version,

            state=
                aggregate.snapshot_state()

        )