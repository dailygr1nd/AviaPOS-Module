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

from modules.expenses.commands import (
    CreateExpenseCommand,
    ApproveExpenseCommand,
    PayExpenseCommand
)


class CreateExpenseCommandHandler:

    def handle(
        self,
        command: CreateExpenseCommand
    ):

        if command.amount <= 0:

            raise ValueError(
                "Expense amount must be positive."
            )

        with UnitOfWork() as uow:

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

                version=1

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

            return {

                "success": True,

                "expense_id":
                    expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }


class ApproveExpenseCommandHandler:

    def handle(
        self,
        command: ApproveExpenseCommand
    ):

        if not command.expense_id:

            raise ValueError(
                "Expense ID is required."
            )

        with UnitOfWork() as uow:

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

                version=1

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

            return {

                "success": True,

                "expense_id":
                    command.expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }


class PayExpenseCommandHandler:

    def handle(
        self,
        command: PayExpenseCommand
    ):

        if not command.expense_id:

            raise ValueError(
                "Expense ID is required."
            )

        if not command.payment_method:

            raise ValueError(
                "Payment method is required."
            )

        with UnitOfWork() as uow:

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

                version=1

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

            return {

                "success": True,

                "expense_id":
                    command.expense_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type

            }