from domain.common.snapshotable import (
    SnapshotableAggregate
)


class ExpenseAggregate(
    SnapshotableAggregate
):

    def __init__(
        self,
        expense_id: str
    ):

        self.id = expense_id

        self.status = "PENDING"

        self.version = 0

    def approve(self):

        if self.status != "PENDING":

            raise ValueError(
                "Expense already processed."
            )

    def pay(self):

        if self.status != "APPROVED":

            raise ValueError(
                "Expense must be approved first."
            )

    def snapshot_state(self):

        return {

            "id": self.id,

            "status": self.status,

            "version": self.version

        }

    def restore_state(

        self,

        state

    ):

        self.id = state["id"]

        self.status = state["status"]

        self.version = state["version"]