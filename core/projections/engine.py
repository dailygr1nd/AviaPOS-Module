from core.ledger.repository import (
    get_all_events
)


class ProjectionEngine:

    def __init__(self):

        self.projectors = []

    def register(
        self,
        projector
    ):

        self.projectors.append(
            projector
        )

    def rebuild(self):

        events = (
            get_all_events()
        )

        for projector in (
            self.projectors
        ):

            projector.reset()

        for event in events:

            for projector in (
                self.projectors
            ):

                projector.apply(
                    event
                )