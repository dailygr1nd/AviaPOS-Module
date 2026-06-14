class SyncQueue:

    def __init__(self):

        self.queue = []

    def push(

        self,

        event

    ):

        self.queue.append(
            event
        )

    def pop(self):

        if not self.queue:

            return None

        return self.queue.pop(0)

    def size(self):

        return len(
            self.queue
        )