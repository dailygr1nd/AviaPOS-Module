from core.events.types import (
    EventType
)

from modules.branches.projection import (
    branches
)


class BranchProjector:

    @staticmethod
    def reset():

        branches.clear()

    @staticmethod
    def apply(event):

        if (

            event["event_type"]

            !=

            EventType
            .BRANCH_CREATED
            .value

        ):

            return

        payload = event[
            "payload"
        ]

        branches[
            payload[
                "branch_id"
            ]
        ] = payload