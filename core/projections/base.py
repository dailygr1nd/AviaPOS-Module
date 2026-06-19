class BaseProjector:

    def reset(self):

        raise NotImplementedError

    def apply(
        self,
        event
    ):

        raise NotImplementedError