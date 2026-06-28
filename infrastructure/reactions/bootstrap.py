import threading

from infrastructure.reactions.purchase_reaction_worker import (
    start_purchase_reaction_worker
)

from infrastructure.reactions.sales_reaction_worker import (
    start_sales_reaction_worker
)


def _launch_worker(target):
    thread = threading.Thread(
        target=target,
        daemon=True
    )

    thread.start()

    return thread


def launch_reaction_workers():
    _launch_worker(
        start_sales_reaction_worker
    )

    _launch_worker(
        start_purchase_reaction_worker
    )