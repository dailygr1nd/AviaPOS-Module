from datetime import datetime

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from infrastructure.idempotency.models import (
    IdempotencyRecordModel
)


class IdempotencyConflict(
    Exception
):

    pass


class IdempotencyInProgress(
    Exception
):

    pass


class IdempotencyRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def get(

        self,

        merchant_id: str,

        idempotency_key: str

    ):

        return (

            self.db.query(
                IdempotencyRecordModel
            )

            .filter(
                IdempotencyRecordModel.merchant_id
                == merchant_id,

                IdempotencyRecordModel.idempotency_key
                == idempotency_key

            )

            .first()

        )

    def start(

        self,

        merchant_id: str,

        idempotency_key: str,

        command_name: str,

        request_hash: str

    ):

        existing = self.get(

            merchant_id,

            idempotency_key

        )

        if existing:

            if existing.request_hash != request_hash:

                raise IdempotencyConflict(

                    "Idempotency key was already used with a different request."

                )

            if existing.status == "COMPLETED":

                return existing, False

            if existing.status == "PENDING":

                raise IdempotencyInProgress(

                    "Request with this idempotency key is already in progress."

                )

            if existing.status == "FAILED":

                raise IdempotencyConflict(

                    "Idempotency key belongs to a failed request. Use a new key."

                )

        record = IdempotencyRecordModel(

            merchant_id=merchant_id,

            idempotency_key=idempotency_key,

            command_name=command_name,

            request_hash=request_hash,

            status="PENDING"

        )

        self.db.add(
            record
        )

        try:

            self.db.flush()

        except IntegrityError:

            self.db.rollback()

            existing = self.get(

                merchant_id,

                idempotency_key

            )

            if existing:

                if existing.request_hash != request_hash:

                    raise IdempotencyConflict(

                        "Idempotency key was already used with a different request."

                    )

                if existing.status == "COMPLETED":

                    return existing, False

                raise IdempotencyInProgress(

                    "Request with this idempotency key is already in progress."

                )

            raise

        return record, True

    def complete(

        self,

        record: IdempotencyRecordModel,

        response_payload: dict

    ):

        record.status = "COMPLETED"

        record.response_payload = response_payload

        record.completed_at = datetime.utcnow()

        self.db.flush()

        return record

    def fail(

        self,

        record: IdempotencyRecordModel,

        error: Exception

    ):

        record.status = "FAILED"

        record.error_message = str(
            error
        )

        self.db.flush()

        return record