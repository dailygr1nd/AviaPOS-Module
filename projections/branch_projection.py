class BranchProjection:

    def __init__(self):

        self.transfers = []

    def apply(

        self,

        event

    ):

        if (

            event["event_type"]

            ==

            "BRANCH_TRANSFER_CREATED"

        ):

            self.transfers.append(

                event["payload"]

            )

    def all_transfers(self):

        return self.transfers