from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.event_store.repository import (
    EventRepository
)

from infrastructure.outbox.repository import (
    OutboxRepository
)

from infrastructure.idempotency.repository import (
    IdempotencyRepository
)


class UnitOfWork:

    def __init__(
        self,
        session_factory=SessionLocal
    ):

        self.session_factory = session_factory

        self.db = None

        self.events = None

        self.outbox = None

        self.idempotency = None

    def __enter__(self):

        self.db = self.session_factory()

        self.events = EventRepository(
            self.db
        )

        self.outbox = OutboxRepository(
            self.db
        )

        self.idempotency = IdempotencyRepository(
            self.db
        )

        return self

    def commit(self):

        self.db.commit()

    def rollback(self):

        self.db.rollback()

    def close(self):

        self.db.close()

    def __exit__(

        self,

        exc_type,

        exc_value,

        traceback

    ):

        try:

            if exc_type:

                self.rollback()

            else:

                self.commit()

        finally:

            self.close()