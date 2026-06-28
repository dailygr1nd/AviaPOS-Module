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

from modules.expenses.commands import (
    CreateExpenseCommand,
    ApproveExpenseCommand,
    PayExpenseCommand
)


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


class CreateExpenseCommandHandler:

    def handle(
        self,
        command: CreateExpenseCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.amount <= 0:

            raise ValueError(
                "Expense amount must be positive."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "category":
                    command.category,

                "description":
                    command.description,

                "amount":
                    command.amount,

                "reference":
                    command.reference

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
                        "CreateExpenseCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            expense_id = str(
                uuid.uuid4()
            )

            payload = {

                "expense_id":
                    expense_id,

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "category":
                    command.category,

                "description":
                    command.description,

                "amount":
                    command.amount,

                "reference":
                    command.reference

            }

            event = create_event(

                EventType.EXPENSE_CREATED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    expense_id,

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

                "expense_id":
                    expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response


class ApproveExpenseCommandHandler:

    def handle(
        self,
        command: ApproveExpenseCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.merchant_id:

            raise ValueError(
                "Merchant ID is required."
            )

        if not command.expense_id:

            raise ValueError(
                "Expense ID is required."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "expense_id":
                    command.expense_id

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
                        "ApproveExpenseCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            payload = {

                "expense_id":
                    command.expense_id

            }

            event = create_event(

                EventType.EXPENSE_APPROVED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.expense_id,

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

                "expense_id":
                    command.expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response


class PayExpenseCommandHandler:

    def handle(
        self,
        command: PayExpenseCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.merchant_id:

            raise ValueError(
                "Merchant ID is required."
            )

        if not command.expense_id:

            raise ValueError(
                "Expense ID is required."
            )

        if not command.payment_method:

            raise ValueError(
                "Payment method is required."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "expense_id":
                    command.expense_id,

                "payment_method":
                    command.payment_method

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
                        "PayExpenseCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            payload = {

                "expense_id":
                    command.expense_id,

                "payment_method":
                    command.payment_method

            }

            event = create_event(

                EventType.EXPENSE_PAID,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    command.expense_id,

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

                "expense_id":
                    command.expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response