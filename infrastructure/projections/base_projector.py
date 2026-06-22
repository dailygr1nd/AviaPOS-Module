class BaseProjector:

    projection_name = None

    def handle(
        self,
        event
    ):
        raise NotImplementedError