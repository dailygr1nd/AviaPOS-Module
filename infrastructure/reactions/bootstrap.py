import importlib
import threading


REACTION_WORKERS = [
    (
        "infrastructure.reactions.sales_reaction_worker",
        "start_sales_reaction_worker"
    ),
    (
        "infrastructure.reactions.purchase_reaction_worker",
        "start_purchase_reaction_worker"
    ),
    (
        "infrastructure.reactions.transfer_reaction_worker",
        "start_transfer_reaction_worker"
    ),
    (
        "infrastructure.reactions.payment_capture_reaction_worker",
        "start_payment_capture_reaction_worker"
    )
    ]


def _launch_worker(target):
    thread = threading.Thread(
        target=target,
        daemon=True
    )

    thread.start()

    return thread


def _load_worker(module_path: str, function_name: str):
    module = importlib.import_module(
        module_path
    )

    return getattr(
        module,
        function_name
    )


def launch_reaction_workers():
    launched = []

    for module_path, function_name in REACTION_WORKERS:
        try:
            target = _load_worker(
                module_path,
                function_name
            )

            launched.append(
                _launch_worker(target)
            )

        except Exception as exc:
            print(
                f"Reaction worker skipped: {module_path}.{function_name}: {exc}"
            )

    return launched