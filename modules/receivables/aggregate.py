from domain.common.snapshotable import (
    SnapshotableAggregate
)


class ReceivableAggregate(
    SnapshotableAggregate
):

    def __init__(

        self,

        receivable_id: str

    ):

        self.id = receivable_id

        self.amount = 0

        self.paid_amount = 0

        self.status = "OPEN"

        self.version = 0

    def snapshot_state(self):

        return {

            "id": self.id,

            "amount": self.amount,

            "paid_amount": self.paid_amount,

            "status": self.status,

            "version": self.version

        }

    def restore_state(

        self,

        state

    ):

        self.id = state["id"]

        self.amount = state["amount"]

        self.paid_amount = state["paid_amount"]

        self.status = state["status"]

        self.version = state["version"]