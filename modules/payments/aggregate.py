from domain.common.snapshotable import (
    SnapshotableAggregate
)

from modules.payments.constants import (
    PaymentStatus
)

from modules.payments.policy_engine import (
    PaymentPolicyEngine
)


class PaymentAggregate(
    SnapshotableAggregate
):

    def __init__(

        self,

        payment_id: str

    ):

        self.id = payment_id

        self.status = (
            PaymentStatus.PENDING
        )

        self.version = 0

    def complete(self):

        PaymentPolicyEngine.validate_transition(

            self.status,

            PaymentStatus.COMPLETED

        )

        self.status = (

            PaymentStatus.COMPLETED
        )

        self.version += 1

    def fail(self):

        PaymentPolicyEngine.validate_transition(

            self.status,

            PaymentStatus.FAILED

        )

        self.status = (
            PaymentStatus.FAILED
        )

        self.version += 1

    def cancel(self):

        PaymentPolicyEngine.validate_transition(

            self.status,

            PaymentStatus.CANCELLED

        )

        self.status = (
            PaymentStatus.CANCELLED
        )

        self.version += 1

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