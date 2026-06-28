from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN_IMPORTS = [

    "from app_context import",
    "import app_context",

    "from storage.sqlite",
    "import storage.sqlite",

    "from infrastructure.queue",
    "import infrastructure.queue",

    "from modules.sales.service",
    "from modules.inventory.service",
    "from modules.payments.service",
    "from modules.receivables.service",

    "from modules.debts",
    "import modules.debts",

    "from core.ledger.store",
    "import core.ledger.store"

]


QUARANTINE_PREFIXES = (

    "application/",
    "storage/sqlite/",
    "modules/debts/",
    "projections/",
    "core/projections/"

)


QUARANTINE_FILES = {

    "app_context.py",

    "scripts/legacy_import_scan.py",

    "core/ledger/store.py",
    "core/ledger/repository.py",
    "core/ledger/hash_chain.py",
    "core/ledger/merchant_ledger.py",

    "modules/branches/service.py",
    "modules/customers/service.py",
    "modules/inventory/service.py",
    "modules/payments/service.py",
    "modules/products/service.py",
    "modules/purchases/service.py",
    "modules/receivables/service.py",
    "modules/sales/service.py",
    "modules/suppliers/service.py",
    "modules/transfers/service.py"

}


def normalized(
    path: Path
) -> str:

    return path.relative_to(
        ROOT
    ).as_posix()


def is_quarantined(
    path: Path
) -> bool:

    value = normalized(
        path
    )

    if value in QUARANTINE_FILES:

        return True

    return any(

        value.startswith(
            prefix
        )

        for prefix in QUARANTINE_PREFIXES

    )


def main():

    violations = []

    for path in ROOT.rglob(
        "*.py"
    ):

        if is_quarantined(
            path
        ):

            continue

        try:

            text = path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            continue

        for forbidden in FORBIDDEN_IMPORTS:

            if forbidden in text:

                violations.append(
                    (
                        normalized(path),
                        forbidden
                    )
                )

    if violations:

        print(
            "Forbidden legacy imports found:\n"
        )

        for file_path, forbidden in violations:

            print(
                f"- {file_path}: {forbidden}"
            )

        sys.exit(1)

    print(
        "No forbidden legacy imports found in active code."
    )


if __name__ == "__main__":

    main()