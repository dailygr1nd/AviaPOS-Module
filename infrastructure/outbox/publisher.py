from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.outbox.repository import (
    OutboxRepository
)

from infrastructure.redis.streams import (
    publish_outbox_message
)


class OutboxPublisher:

    def __init__(
        self,
        session_factory=SessionLocal
    ):

        self.session_factory = session_factory

    def publish_pending(

        self,

        limit: int = 100

    ):

        db = self.session_factory()

        repo = OutboxRepository(
            db
        )

        published = 0

        failed = 0

        try:

            messages = repo.get_pending(
                limit=limit
            )

            for message in messages:

                try:

                    publish_outbox_message(
                        message.payload
                    )

                    repo.mark_published(
                        message
                    )

                    db.commit()

                    published += 1

                except Exception as exc:

                    db.rollback()

                    db = self.session_factory()

                    repo = OutboxRepository(
                        db
                    )

                    fresh_message = (

                        db.query(
                            type(message)
                        )

                        .filter(
                            type(message).id
                            == message.id
                        )

                        .first()

                    )

                    if fresh_message:

                        repo.mark_failed(
                            fresh_message,
                            exc
                        )

                        db.commit()

                    failed += 1

            return {

                "published":
                    published,

                "failed":
                    failed

            }

        finally:

            db.close()