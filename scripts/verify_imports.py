from pathlib import Path

import importlib
import os
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )

os.chdir(
    PROJECT_ROOT
)
ACTIVE_IMPORTS = [

    "main",

    "api.auth.security",
    "api.auth.dependencies",

    "core.commands.command",
    "core.commands.command_bus",
    "core.commands.registry",

    "core.events.base",
    "core.events.hash",
    "core.events.types",

    "core.ledger.event_factory",

    "infrastructure.database.base",
    "infrastructure.database.connection",
    "infrastructure.database.session",
    "infrastructure.database.unit_of_work",

    "infrastructure.event_store.models",
    "infrastructure.event_store.repository",

    "infrastructure.outbox.models",
    "infrastructure.outbox.repository",
    "infrastructure.outbox.publisher",

    "infrastructure.idempotency.models",
    "infrastructure.idempotency.repository",
    "infrastructure.idempotency.request_hash",

    "infrastructure.concurrency.exceptions",

    "infrastructure.redis.client",
    "infrastructure.redis.consumer",
    "infrastructure.redis.streams",
    "infrastructure.redis.bootstrap",

    "infrastructure.projections.redis_worker",

    "infrastructure.reactions.sales_reaction_worker",
    "infrastructure.reactions.bootstrap",

    "modules.users.api",
    "modules.users.models",
    "modules.users.repository",
    "modules.users.schemas",
    "modules.users.service",

    "modules.dashboard.api",
    "modules.dashboard.query_service",
    "modules.dashboard.schemas",

    "modules.sales.api",
    "modules.sales.commands",
    "modules.sales.command_handlers",
    "modules.sales.models",
    "modules.sales.projector",
    "modules.sales.query_service",
    "modules.sales.reactions",
    "modules.sales.schemas",

    "modules.inventory.api",
    "modules.inventory.commands",
    "modules.inventory.command_handlers",
    "modules.inventory.models",
    "modules.inventory.projector",
    "modules.inventory.query_service",
    "modules.inventory.schemas",

    "modules.expenses.api",
    "modules.expenses.commands",
    "modules.expenses.command_handlers",
    "modules.expenses.models",
    "modules.expenses.projector",
    "modules.expenses.query_service",
    "modules.expenses.schemas",

    "modules.products.api",
    "modules.products.commands",
    "modules.products.command_handlers",
    "modules.products.models",
    "modules.products.projector",
    "modules.products.query_service",
    "modules.products.schemas",

    "modules.payments.api",
    "modules.payments.commands",
    "modules.payments.command_handlers",
    "modules.payments.constants",
    "modules.payments.models",
    "modules.payments.projector",
    "modules.payments.query_service",
    "modules.payments.reference_registry",
    "modules.payments.schemas",


    "modules.customers.api",
    "modules.customers.commands",
    "modules.customers.command_handlers",
    "modules.customers.models",
    "modules.customers.projector",
    "modules.customers.query_service",
    "modules.customers.schemas",

    "modules.receivables.api",
    "modules.receivables.commands",
    "modules.receivables.command_handlers",
    "modules.receivables.models",
    "modules.receivables.projector",
    "modules.receivables.query_service",
    "modules.receivables.schemas",

    "modules.sync.api",
    "modules.sync.models",
    "modules.sync.repository",
    "modules.sync.schemas",

  
    "modules.control_center.api_integrity",
    

]


def main():

    failed = []

    for module_name in ACTIVE_IMPORTS:

        try:

            importlib.import_module(
                module_name
            )

            print(
                f"OK   {module_name}"
            )

        except Exception as exc:

            failed.append(
                (
                    module_name,
                    exc
                )
            )

            print(
                f"FAIL {module_name}: {exc}"
            )

    if failed:

        print(
            "\nImport smoke test failed:\n"
        )

        for module_name, exc in failed:

            print(
                f"- {module_name}: {exc}"
            )

        sys.exit(1)

    print(
        "\nAll active imports passed."
    )


if __name__ == "__main__":

    main()