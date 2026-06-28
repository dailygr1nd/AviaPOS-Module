import threading

from infrastructure.reactions.sales_reaction_worker import (
    start_sales_reaction_worker
)


def launch_reaction_workers():

    thread = threading.Thread(

        target=start_sales_reaction_worker,

        daemon=True

    )

    thread.start()