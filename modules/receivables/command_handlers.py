import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

from infrastructure.database.unit_of_work import (
    UnitOfWork
)

from infrastructure.idempotency.request_hash import (
    calculate_request_hash
)

from modules.receivables.commands import (
    CreateReceivableCommand,
    RecordReceivablePaymentCommand
)


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


class CreateReceivableCommandHandler:

    def handle(
        self,
        command: CreateReceivableCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.amount <= 0:

            raise ValueError(
                "Receivable amount must be positive."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "customer_id":
                    command.customer_id,

                "sale_id":
                    command.sale_id,

                "amount":
                    command.amount

            }

        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "CreateReceivableCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            receivable_id = str(
                uuid.uuid4()
            )

            payload = {

                "receivable_id":
                    receivable_id,

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "customer_id":
                    command.customer_id,

                "sale_id":
                    command.sale_id,

                "amount":
                    command.amount

            }

            event = create_event(

                EventType.RECEIVABLE_CREATED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    receivable_id,

                version=1,

                metadata={

                    "idempotency_key":
                        command.idempotency_key

                }

            )

            persisted_event = uow.events.append(

                event,

                commit=False

            )

            uow.outbox.add_event(

                event,

                persisted_event_id=
                    persisted_event.id

            )

            response = {

                "success": True,

                "receivable_id":
                    receivable_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response


class RecordReceivablePaymentCommandHandler:

    def handle(
        self,
        command: RecordReceivablePaymentCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.merchant_id:

            raise ValueError(
                "Merchant ID is required."
            )

        if not command.receivable_id:

            raise ValueError(
                "Receivable ID is required."
            )

        if command.amount <= 0:

            raise ValueError(
                "Payment amount must be positive."
            )

        if not command.payment_method:

            raise ValueError(
                "Payment method is required."
            )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "receivable_id":
                    command.receivable_id,

                "amount":
                    command.amount,

                "payment_method":
                    command.payment_method,

                "expected_version":
                    command.expected_version

            }

        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "RecordReceivablePaymentCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            current_version = uow.events.assert_expected_version(

                merchant_id=
                    command.merchant_id,

                aggregate_id=
                    command.receivable_id,

                expected_version=
                    command.expected_version

            )

            next_version = current_version + 1

            payload = {

                "receivable_id":
                    command.receivable_id,

                "amount":
                    command.amount,

                "payment_method":
                    command.payment_method

            }

            event = create_event(

                EventType.RECEIVABLE_PAYMENT_RECORDED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.receivable_id,

                version=
                    next_version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key,

                    "expected_version":
                        command.expected_version

                }

            )

            persisted_event = uow.events.append(

                event,

                commit=False

            )

            uow.outbox.add_event(

                event,

                persisted_event_id=
                    persisted_event.id

            )

            response = {

                "success": True,

                "receivable_id":
                    command.receivable_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response