from collections import defaultdict


class EventBus:

    def __init__(self):

        self.handlers = defaultdict(list)

    def subscribe(

        self,

        event_type: str,

        handler

    ):

        self.handlers[event_type].append(
            handler
        )

    def publish(

        self,

        event

    ):

        handlers = self.handlers.get(

            event.event_type,

            []

        )

        for handler in handlers:

            handler(event)


event_bus = EventBus()