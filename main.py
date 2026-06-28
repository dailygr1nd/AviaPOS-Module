from fastapi import FastAPI

from core.commands.registry import (
    register_command_handlers
)

from infrastructure.outbox.bootstrap import (
    launch_outbox_worker
)

from infrastructure.redis.bootstrap import (
    bootstrap_redis
)

from infrastructure.redis.start_worker import (
    launch_workers
)

from modules.branches.api import router as branches_router
from modules.customers.api import router as customers_router
from modules.expenses.api import router as expenses_router
from modules.inventory.api import router as inventory_router
from modules.payments.api import router as payments_router
from modules.products.api import router as products_router
from modules.purchases.api import router as purchases_router
from modules.receivables.api import router as receivables_router
from modules.sales.api import router as sales_router
from modules.suppliers.api import router as suppliers_router
from modules.sync.api import router as sync_router
from modules.transfers.api import router as transfers_router
from modules.users.api import router as auth_router

from modules.control_center.api import router as control_router
from modules.control_center.api_debug import router as debug_router
from modules.control_center.api_integrity import router as integrity_router
from modules.control_center.api_trace import router as trace_router


app = FastAPI(

    title="AviaPOS",

    version="0.6.0"

)


@app.on_event("startup")
def startup():

    register_command_handlers()

    try:

        bootstrap_redis()

        launch_workers()

        launch_outbox_worker()

    except Exception as exc:

        print(
            f"Background worker startup skipped: {exc}"
        )


app.include_router(
    auth_router
)

app.include_router(
    sales_router,
    prefix="/sales",
    tags=["Sales"]
)

app.include_router(
    inventory_router,
    prefix="/inventory",
    tags=["Inventory"]
)

app.include_router(
    products_router,
    prefix="/products",
    tags=["Products"]
)

app.include_router(
    customers_router,
    prefix="/customers",
    tags=["Customers"]
)

app.include_router(
    branches_router,
    prefix="/branches",
    tags=["Branches"]
)

app.include_router(
    suppliers_router,
    prefix="/suppliers",
    tags=["Suppliers"]
)

app.include_router(
    purchases_router,
    prefix="/purchases",
    tags=["Purchases"]
)

app.include_router(
    transfers_router,
    prefix="/transfers",
    tags=["Transfers"]
)

app.include_router(
    expenses_router
)

app.include_router(
    payments_router
)

app.include_router(
    receivables_router
)

app.include_router(
    sync_router
)

app.include_router(
    control_router,
    prefix="/control",
    tags=["Control Center"]
)

app.include_router(
    trace_router,
    prefix="/control",
    tags=["Tracing"]
)

app.include_router(
    debug_router,
    prefix="/control",
    tags=["Debug"]
)

app.include_router(
    integrity_router,
    prefix="/control",
    tags=["Integrity"]
)