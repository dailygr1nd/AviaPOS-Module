class BranchProjection:

    def __init__(self):

        self.transfers = []

    def apply(self, event):

        if (

            event["event_type"]

            ==

            "BRANCH_TRANSFER_CREATED"

        ):

            self.transfers.append(

                event["payload"]

            )

    def replay(self, events):

        for event in events:

            self.apply(event)