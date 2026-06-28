from pydantic import BaseModel


class DashboardWarning(
    BaseModel
):

    code: str

    message: str

    severity: str


class DashboardSummary(
    BaseModel
):

    merchant_id: str

    branch_id: str | None = None

    sales: dict

    inventory: dict

    cashflow: dict

    receivables: dict

    expenses: dict

    payments: dict

    warnings: list[DashboardWarning]