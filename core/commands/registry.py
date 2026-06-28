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
    
    from modules.purchases.commands import (
    CancelPurchaseCommand,
    CreatePurchaseCommand,
    ReceivePurchaseCommand
    )

    from modules.purchases.command_handlers import (
    CancelPurchaseCommandHandler,
    CreatePurchaseCommandHandler,
    ReceivePurchaseCommandHandler
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

    from modules.customers.commands import (
        CreateCustomerCommand,
        DeactivateCustomerCommand,
        UpdateCustomerCommand
    )

    from modules.customers.command_handlers import (
        CreateCustomerCommandHandler,
        DeactivateCustomerCommandHandler,
        UpdateCustomerCommandHandler
    )

    from modules.branches.commands import (
        CreateBranchCommand,
        DeactivateBranchCommand,
        UpdateBranchCommand
    )

    from modules.branches.command_handlers import (
        CreateBranchCommandHandler,
        DeactivateBranchCommandHandler,
        UpdateBranchCommandHandler
    )

    from modules.suppliers.commands import (
    CreateSupplierCommand,
    DeactivateSupplierCommand,
    UpdateSupplierCommand
    )

    from modules.suppliers.command_handlers import (
    CreateSupplierCommandHandler,
    DeactivateSupplierCommandHandler,
    UpdateSupplierCommandHandler
    )


    command_bus.register(

        CreateExpenseCommand,

        CreateExpenseCommandHandler()

    )
    command_bus.register(
    CreateSupplierCommand,
    CreateSupplierCommandHandler()
    )

    command_bus.register(
    UpdateSupplierCommand,
    UpdateSupplierCommandHandler()
    )

    command_bus.register(
    DeactivateSupplierCommand,
    DeactivateSupplierCommandHandler()
    )


    command_bus.register(

        ApproveExpenseCommand,

        ApproveExpenseCommandHandler()

    )

    command_bus.register(
        CreateBranchCommand,
        CreateBranchCommandHandler()
    )

    command_bus.register(
        UpdateBranchCommand,
        UpdateBranchCommandHandler()
    )

    command_bus.register(
        DeactivateBranchCommand,
        DeactivateBranchCommandHandler()
    )

    command_bus.register(

        PayExpenseCommand,

        PayExpenseCommandHandler()

    )

    command_bus.register(
    CreatePurchaseCommand,
    CreatePurchaseCommandHandler()
    )

    command_bus.register(
    ReceivePurchaseCommand,
    ReceivePurchaseCommandHandler()
    )

    command_bus.register(
    CancelPurchaseCommand,
    CancelPurchaseCommandHandler()
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

    command_bus.register(

        CreateCustomerCommand,

        CreateCustomerCommandHandler()

    )

    command_bus.register(

        UpdateCustomerCommand,

        UpdateCustomerCommandHandler()

    )

    command_bus.register(

        DeactivateCustomerCommand,

        DeactivateCustomerCommandHandler()

    )

    _registered = True

    return command_bus