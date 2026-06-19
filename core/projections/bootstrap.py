from core.projections.registry import (
    engine
)

from modules.inventory.projector import (
    InventoryProjector
)

from modules.sales.projector import (
    SalesProjector
)

from modules.customers.projector import (
    CustomerProjector
)

from modules.debts.projector import (
    DebtProjector
)

from modules.suppliers.projector import (
    SupplierProjector
)

from modules.branches.projector import (
    BranchProjector
)


engine.register(
    InventoryProjector()
)

engine.register(
    SalesProjector()
)

engine.register(
    CustomerProjector()
)

engine.register(
    DebtProjector()
)

engine.register(
    SupplierProjector()
)

engine.register(
    BranchProjector()
)