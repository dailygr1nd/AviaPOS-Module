class DashboardProjection:

    def __init__(

        self,

        sales_projection,

        debt_projection,

        inventory_projection

    ):

        self.sales_projection = (
            sales_projection
        )

        self.debt_projection = (
            debt_projection
        )

        self.inventory_projection = (
            inventory_projection
        )

    def snapshot(self):

        return {

            "sales_total":

                self.sales_projection
                .total(),

            "sales_count":

                self.sales_projection
                .count(),

            "customer_debt":

                sum(

                    self.debt_projection
                    .balances.values()

                ),

            "tracked_products":

                len(

                    self.inventory_projection
                    .stock

                )
        }