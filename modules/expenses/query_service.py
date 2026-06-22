from infrastructure.database.session import (
    SessionLocal
)

from modules.expenses.models import (
    ExpenseProjection
)


def get_expenses(

    merchant_id: str

):

    db = SessionLocal()

    return (

        db.query(
            ExpenseProjection
        )

        .filter(
            ExpenseProjection.merchant_id
            == merchant_id
        )

        .all()

    )


def get_expense_summary(

    merchant_id: str

):

    db = SessionLocal()

    expenses = (

        db.query(
            ExpenseProjection
        )

        .filter(
            ExpenseProjection.merchant_id
            == merchant_id
        )

        .all()

    )

    total = sum(
        x.amount
        for x in expenses
    )

    return {

        "total_expenses":
            total,

        "count":
            len(expenses)

    }