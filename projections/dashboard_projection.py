from projections.sales_projection import (
    SalesProjection
)

from projections.inventory_projection import (
    InventoryProjection
)

from projections.debt_projection import (
    DebtProjection
)

from projections.expense_projection import (
    ExpenseProjection
)

from projections.branch_projection import (
    BranchProjection
)


class DashboardProjection:

    def build(

        self,

        events

    ):

        sales = SalesProjection()

        inventory = InventoryProjection()

        debt = DebtProjection()

        expenses = ExpenseProjection()

        branches = BranchProjection()

        sales.replay(events)

        inventory.replay(events)

        debt.replay(events)

        expenses.replay(events)

        branches.replay(events)

        return {

            "total_sales":

                sales.total(),

            "sales_count":

                sales.count(),

            "products_tracked":

                len(
                    inventory.stock
                ),

            "inventory_units":

                sum(
                    inventory.stock.values()
                ),

            "outstanding_debt":

                sum(
                    debt.balances.values()
                ),

            "expenses":

                expenses.total_expenses,

            "branch_transfers":

                len(
                    branches.transfers
                )

        }