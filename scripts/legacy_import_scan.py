from pathlib import Path
import sys


ROOT = Path(
    "."
)

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


IGNORED_PREFIXES = (

    "application/",
    "storage/sqlite/",
    "modules/debts/",
    "projections/",
    "api/schemas/"

)


IGNORED_FILES = {

    "app_context.py",
    "core/ledger/store.py",
    "core/ledger/repository.py",
    "core/ledger/hash_chain.py",
    "core/ledger/merchant_ledger.py",
    "core/events/bus.py",
    "core/events/event_bus.py"

}


def normalized(
    path: Path
) -> str:

    return path.as_posix()


def is_ignored(
    path: Path
) -> bool:

    value = normalized(
        path
    )

    if value in IGNORED_FILES:

        return True

    return any(

        value.startswith(
            prefix
        )

        for prefix in IGNORED_PREFIXES

    )


def main():

    violations = []

    for path in ROOT.rglob(
        "*.py"
    ):

        value = normalized(
            path
        )

        if is_ignored(
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
                        value,
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