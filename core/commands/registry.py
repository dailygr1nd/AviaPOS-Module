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
        ApproveExpenseCommand,
        CreateExpenseCommand,
        PayExpenseCommand
    )

    from modules.expenses.command_handlers import (
        ApproveExpenseCommandHandler,
        CreateExpenseCommandHandler,
        PayExpenseCommandHandler
    )

    from modules.payments.commands import (
        CancelPaymentCommand,
        CompletePaymentCommand,
        CreatePaymentCommand,
        FailPaymentCommand
    )

    from modules.payments.command_handlers import (
        CancelPaymentCommandHandler,
        CompletePaymentCommandHandler,
        CreatePaymentCommandHandler,
        FailPaymentCommandHandler
    )

    from modules.receivables.commands import (
        CreateReceivableCommand,
        RecordReceivablePaymentCommand
    )

    from modules.receivables.command_handlers import (
        CreateReceivableCommandHandler,
        RecordReceivablePaymentCommandHandler
    )

    from modules.inventory.commands import (
        AdjustInventoryCommand,
        DeductInventoryCommand,
        ReceiveInventoryCommand
    )

    from modules.inventory.command_handlers import (
        AdjustInventoryCommandHandler,
        DeductInventoryCommandHandler,
        ReceiveInventoryCommandHandler
    )

    from modules.sales.commands import (
        CreateSaleCommand
    )

    from modules.sales.command_handlers import (
        CreateSaleCommandHandler
    )

    from modules.products.commands import (
        CreateProductCommand,
        DeactivateProductCommand,
        UpdateProductCommand
    )

    from modules.products.command_handlers import (
        CreateProductCommandHandler,
        DeactivateProductCommandHandler,
        UpdateProductCommandHandler
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

    command_bus.register(

        ReceiveInventoryCommand,

        ReceiveInventoryCommandHandler()

    )

    command_bus.register(

        DeductInventoryCommand,

        DeductInventoryCommandHandler()

    )

    command_bus.register(

        AdjustInventoryCommand,

        AdjustInventoryCommandHandler()

    )

    command_bus.register(

        CreateSaleCommand,

        CreateSaleCommandHandler()

    )

    command_bus.register(

        CreateProductCommand,

        CreateProductCommandHandler()

    )

    command_bus.register(

        UpdateProductCommand,

        UpdateProductCommandHandler()

    )

    command_bus.register(

        DeactivateProductCommand,

        DeactivateProductCommandHandler()

    )

    _registered = True

    return command_bus