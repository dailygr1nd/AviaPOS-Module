from fastapi import FastAPI

from core.commands.registry import (
    register_command_handlers
)

from infrastructure.outbox.bootstrap import (
    launch_outbox_worker
)

from infrastructure.reactions.bootstrap import (
    launch_reaction_workers
)

from infrastructure.redis.bootstrap import (
    bootstrap_redis
)

from infrastructure.redis.start_worker import (
    launch_workers
)

from modules.dashboard.api import router as dashboard_router
from modules.expenses.api import router as expenses_router
from modules.inventory.api import router as inventory_router
from modules.payments.api import router as payments_router
from modules.products.api import router as products_router
from modules.receivables.api import router as receivables_router
from modules.sales.api import router as sales_router
from modules.sync.api import router as sync_router
from modules.users.api import router as auth_router

from modules.control_center.api_integrity import (
    router as integrity_router
)


app = FastAPI(

    title="AviaPOS",

    version="0.9.1"

)


@app.on_event("startup")
def startup():

    register_command_handlers()

    try:

        bootstrap_redis()

        launch_workers()

        launch_outbox_worker()

        launch_reaction_workers()

    except Exception as exc:

        print(
            f"Background worker startup skipped: {exc}"
        )


app.include_router(
    auth_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    products_router
)

app.include_router(
    sales_router
)

app.include_router(
    inventory_router
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
    integrity_router,
    prefix="/control",
    tags=["Integrity"]
)