from datetime import datetime

from modules.expenses.models import (
    ExpenseProjection
)

from infrastructure.projections.base_projector import (
    BaseProjector
)


class ExpenseProjector(
    BaseProjector
):

    projection_name = (
        "expense_projection"
    )

    def __init__(

        self,

        db

    ):

        self.db = db

    def handle(

        self,

        event

    ):

        if event.event_type == (
            "EXPENSE_CREATED"
        ):

            self.create(
                event.payload
            )

        elif event.event_type == (
            "EXPENSE_APPROVED"
        ):

            self.approve(
                event.payload
            )

        elif event.event_type == (
            "EXPENSE_PAID"
        ):

            self.pay(
                event.payload
            )

    def create(

        self,

        payload

    ):

        row = ExpenseProjection(

            expense_id=
                payload["expense_id"],

            merchant_id=
                payload["merchant_id"],

            branch_id=
                payload["branch_id"],

            category=
                payload["category"],

            description=
                payload["description"],

            amount=
                payload["amount"],

            status="PENDING",

            created_at=
                datetime.utcnow()

        )

        self.db.add(row)

        self.db.commit()

    def approve(

        self,

        payload

    ):

        expense = (

            self.db.query(
                ExpenseProjection
            )

            .filter(
                ExpenseProjection.expense_id
                == payload["expense_id"]
            )

            .first()

        )

        if expense:

            expense.status = (
                "APPROVED"
            )

            self.db.commit()

    def pay(

        self,

        payload

    ):

        expense = (

            self.db.query(
                ExpenseProjection
            )

            .filter(
                ExpenseProjection.expense_id
                == payload["expense_id"]
            )

            .first()

        )

        if expense:

            expense.status = (
                "PAID"
            )

            self.db.commit()