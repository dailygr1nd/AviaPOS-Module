from core.projections.registry import (
    engine
)

from modules.inventory.projection import (
    inventory
)


def get_stock(

    branch_id: str,

    product_id: str

):

    engine.rebuild()

    return inventory.get(

        (

            branch_id,

            product_id

        ),

        0

    )