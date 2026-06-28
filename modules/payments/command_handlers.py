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

from modules.payments.commands import (
    CreatePaymentCommand,
    CompletePaymentCommand,
    FailPaymentCommand,
    CancelPaymentCommand
)

from modules.payments.constants import (
    PaymentReferenceType
)

from modules.payments.reference_registry import (
    PaymentReferenceRegistry
)


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


def _validate_reference_type(
    reference_type: str
):

    try:

        normalized = PaymentReferenceType(
            reference_type
        )

    except ValueError as exc:

        raise ValueError(

            f"Unsupported payment reference type: {reference_type}"

        ) from exc

    PaymentReferenceRegistry.validate(
        normalized
    )

    return normalized.value


class CreatePaymentCommandHandler:

    def handle(
        self,
        command: CreatePaymentCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.amount <= 0:

            raise ValueError(
                "Payment amount must be positive."
            )

        reference_type = _validate_reference_type(
            command.reference_type
        )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "amount":
                    command.amount,

                "payment_method":
                    command.payment_method,

                "reference_type":
                    reference_type,

                "reference_id":
                    command.reference_id,

                "notes":
                    command.notes

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
                        "CreatePaymentCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            payment_id = str(
                uuid.uuid4()
            )

            payload = {

                "payment_id":
                    payment_id,

                "merchant_id":
                    command.merchant_id,

                "amount":
                    command.amount,

                "payment_method":
                    command.payment_method,

                "reference_type":
                    reference_type,

                "reference_id":
                    command.reference_id,

                "notes":
                    command.notes

            }

            event = create_event(

                EventType.PAYMENT_CREATED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    payment_id,

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

                "payment_id":
                    payment_id,

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


class CompletePaymentCommandHandler:

    def handle(
        self,
        command: CompletePaymentCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "payment_id":
                    command.payment_id,

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
                        "CompletePaymentCommand",

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
                    command.payment_id,

                expected_version=
                    command.expected_version

            )

            next_version = current_version + 1

            payload = {

                "payment_id":
                    command.payment_id

            }

            event = create_event(

                EventType.PAYMENT_COMPLETED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.payment_id,

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

                "payment_id":
                    command.payment_id,

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


class FailPaymentCommandHandler:

    def handle(
        self,
        command: FailPaymentCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "payment_id":
                    command.payment_id,

                "reason":
                    command.reason,

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
                        "FailPaymentCommand",

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
                    command.payment_id,

                expected_version=
                    command.expected_version

            )

            next_version = current_version + 1

            payload = {

                "payment_id":
                    command.payment_id,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.PAYMENT_FAILED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.payment_id,

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

                "payment_id":
                    command.payment_id,

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


class CancelPaymentCommandHandler:

    def handle(
        self,
        command: CancelPaymentCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "payment_id":
                    command.payment_id,

                "reason":
                    command.reason,

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
                        "CancelPaymentCommand",

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
                    command.payment_id,

                expected_version=
                    command.expected_version

            )

            next_version = current_version + 1

            payload = {

                "payment_id":
                    command.payment_id,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.PAYMENT_CANCELLED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.payment_id,

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

                "payment_id":
                    command.payment_id,

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