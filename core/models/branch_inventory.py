class BranchInventory:

    def __init__(self):

        self.stock = {}

    def receive(

        self,

        branch_id,

        product_id,

        quantity

    ):

        key = (

            branch_id,

            product_id

        )

        self.stock[key] = (

            self.stock.get(

                key,

                0

            )

            +

            quantity

        )

    def issue(

        self,

        branch_id,

        product_id,

        quantity

    ):

        key = (

            branch_id,

            product_id

        )

        available = self.stock.get(

            key,

            0

        )

        if quantity > available:

            raise ValueError(

                "Insufficient branch stock"

            )

        self.stock[key] = (

            available

            -

            quantity

        )