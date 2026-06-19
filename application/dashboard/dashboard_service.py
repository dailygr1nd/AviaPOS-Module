from app_context import (
    store
)

from projections.sales_projection import (
    SalesProjection
)

from projections.debt_projection import (
    DebtProjection
)

from projections.expense_projection import (
    ExpenseProjection
)

from projections.inventory_projection import (
    InventoryProjection
)


class DashboardService:

    def summary(

        self,

        merchant_id: str

    ):

        events = store.load_events(

            merchant_id

        )

        sales = SalesProjection()

        debt = DebtProjection()

        expense = ExpenseProjection()

        inventory = InventoryProjection()

        for event in events:

            sales.apply(event)

            debt.apply(event)

            expense.apply(event)

            inventory.apply(event)

        return {

            "sales":

                sales.summary(),

            "debt":

                debt.outstanding(),

            "expenses":

                expense.total(),

            "stock":

                inventory.stock

        }