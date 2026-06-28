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

    _registered = True

    return command_bus