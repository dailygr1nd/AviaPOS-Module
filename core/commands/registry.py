from core.commands.command_bus import (
    CommandBus
)


command_bus = CommandBus()

_registered = False


def register_command_handlers():

    global _registered

    if _registered:

        return command_bus

    from modules.expenses.commands import (
        CreateExpenseCommand,
        ApproveExpenseCommand,
        PayExpenseCommand
    )

    from modules.expenses.command_handlers import (
        CreateExpenseCommandHandler,
        ApproveExpenseCommandHandler,
        PayExpenseCommandHandler
    )

    from modules.payments.commands import (
        CreatePaymentCommand,
        CompletePaymentCommand,
        FailPaymentCommand,
        CancelPaymentCommand
    )

    from modules.payments.command_handlers import (
        CreatePaymentCommandHandler,
        CompletePaymentCommandHandler,
        FailPaymentCommandHandler,
        CancelPaymentCommandHandler
    )

    from modules.receivables.commands import (
        CreateReceivableCommand,
        RecordReceivablePaymentCommand
    )

    from modules.receivables.command_handlers import (
        CreateReceivableCommandHandler,
        RecordReceivablePaymentCommandHandler
    )

    command_bus.register(

        CreateExpenseCommand,

        CreateExpenseCommandHandler()

    )

    command_bus.register(

        ApproveExpenseCommand,

        ApproveExpenseCommandHandler()

    )

    command_bus.register(

        PayExpenseCommand,

        PayExpenseCommandHandler()

    )

    command_bus.register(

        CreatePaymentCommand,

        CreatePaymentCommandHandler()

    )

    command_bus.register(

        CompletePaymentCommand,

        CompletePaymentCommandHandler()

    )

    command_bus.register(

        FailPaymentCommand,

        FailPaymentCommandHandler()

    )

    command_bus.register(

        CancelPaymentCommand,

        CancelPaymentCommandHandler()

    )

    command_bus.register(

        CreateReceivableCommand,

        CreateReceivableCommandHandler()

    )

    command_bus.register(

        RecordReceivablePaymentCommand,

        RecordReceivablePaymentCommandHandler()

    )

    _registered = True

    return command_bus