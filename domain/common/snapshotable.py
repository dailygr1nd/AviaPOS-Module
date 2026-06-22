class SnapshotableAggregate:

    def snapshot_state(self):

        raise NotImplementedError

    def restore_state(

        self,

        state: dict

    ):

        raise NotImplementedError