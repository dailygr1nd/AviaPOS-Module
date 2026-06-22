from infrastructure.snapshots.repository import (
    SnapshotRepository
)


class AggregateRebuilder:

    def __init__(

        self,

        snapshot_repo,

        event_repo

    ):

        self.snapshot_repo = snapshot_repo

        self.event_repo = event_repo

    def rebuild(

        self,

        aggregate

    ):

        snapshot = (
            self.snapshot_repo
            .get_latest(
                aggregate.id
            )
        )

        if snapshot:

            aggregate.restore_state(
                snapshot.state
            )

            start_version = (
                snapshot.version
            )

        else:

            start_version = 0

        events = (
            self.event_repo
            .get_events_after_version(

                aggregate.id,

                start_version

            )
        )

        for event in events:

            aggregate.apply(
                event
            )

        return aggregate