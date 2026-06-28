from sqlalchemy import func

from infrastructure.database.session import (
    SessionLocal
)

from modules.expenses.models import (
    ExpenseProjection
)

from modules.inventory.models import (
    InventoryProjection
)

from modules.payments.models import (
    PaymentProjection
)

from modules.receivables.models import (
    ReceivableProjection
)

from modules.sales.models import (
    SaleProjection
)


LOW_STOCK_THRESHOLD = 5


def _safe_number(
    value
):

    if value is None:

        return 0

    return value


def _base_sales_query(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    query = db.query(
        SaleProjection
    ).filter(
        SaleProjection.merchant_id
        == merchant_id
    )

    if branch_id:

        query = query.filter(
            SaleProjection.branch_id
            == branch_id
        )

    return query


def _base_inventory_query(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    query = db.query(
        InventoryProjection
    ).filter(
        InventoryProjection.merchant_id
        == merchant_id
    )

    if branch_id:

        query = query.filter(
            InventoryProjection.branch_id
            == branch_id
        )

    return query


def _base_expense_query(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    query = db.query(
        ExpenseProjection
    ).filter(
        ExpenseProjection.merchant_id
        == merchant_id
    )

    if branch_id:

        query = query.filter(
            ExpenseProjection.branch_id
            == branch_id
        )

    return query


def _base_receivable_query(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    query = db.query(
        ReceivableProjection
    ).filter(
        ReceivableProjection.merchant_id
        == merchant_id
    )

    if branch_id:

        query = query.filter(
            ReceivableProjection.branch_id
            == branch_id
        )

    return query


def _base_payment_query(
    db,
    merchant_id: str
):

    return db.query(
        PaymentProjection
    ).filter(
        PaymentProjection.merchant_id
        == merchant_id
    )


def _sales_summary(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    sales_query = _base_sales_query(
        db,
        merchant_id,
        branch_id
    )

    completed_query = sales_query.filter(
        SaleProjection.status
        == "COMPLETED"
    )

    total_sales_value = _safe_number(

        completed_query.with_entities(
            func.sum(
                SaleProjection.total
            )
        ).scalar()

    )

    completed_count = completed_query.count()

    total_count = sales_query.count()

    average_sale_value = 0

    if completed_count > 0:

        average_sale_value = (

            total_sales_value

            /

            completed_count

        )

    recent_sales = (

        sales_query.order_by(
            SaleProjection.created_at.desc()
        )

        .limit(
            5
        )

        .all()

    )

    return {

        "total_sales_value":
            total_sales_value,

        "completed_count":
            completed_count,

        "total_count":
            total_count,

        "average_sale_value":
            average_sale_value,

        "recent_sales":
            [

                {

                    "sale_id":
                        sale.sale_id,

                    "branch_id":
                        sale.branch_id,

                    "total":
                        sale.total,

                    "status":
                        sale.status,

                    "payment_method":
                        sale.payment_method,

                    "created_at":
                        sale.created_at

                }

                for sale in recent_sales

            ]

    }


def _inventory_summary(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    inventory_query = _base_inventory_query(
        db,
        merchant_id,
        branch_id
    )

    rows = inventory_query.all()

    total_units = sum(
        row.quantity
        for row in rows
    )

    low_stock_items = [

        row

        for row in rows

        if row.quantity <= LOW_STOCK_THRESHOLD

        and row.quantity >= 0

    ]

    negative_stock_items = [

        row

        for row in rows

        if row.quantity < 0

    ]

    return {

        "tracked_items":
            len(
                rows
            ),

        "total_units":
            total_units,

        "low_stock_count":
            len(
                low_stock_items
            ),

        "negative_stock_count":
            len(
                negative_stock_items
            ),

        "low_stock_items":
            [

                {

                    "merchant_id":
                        row.merchant_id,

                    "branch_id":
                        row.branch_id,

                    "product_id":
                        row.product_id,

                    "sku":
                        row.sku,

                    "quantity":
                        row.quantity,

                    "version":
                        row.version

                }

                for row in low_stock_items[:10]

            ]

    }


def _expense_summary(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    expense_query = _base_expense_query(
        db,
        merchant_id,
        branch_id
    )

    total_expenses = _safe_number(

        expense_query.with_entities(
            func.sum(
                ExpenseProjection.amount
            )
        ).scalar()

    )

    paid_expenses = _safe_number(

        expense_query.filter(
            ExpenseProjection.status
            == "PAID"
        )

        .with_entities(
            func.sum(
                ExpenseProjection.amount
            )
        )

        .scalar()

    )

    pending_count = expense_query.filter(
        ExpenseProjection.status
        == "PENDING"
    ).count()

    approved_count = expense_query.filter(
        ExpenseProjection.status
        == "APPROVED"
    ).count()

    paid_count = expense_query.filter(
        ExpenseProjection.status
        == "PAID"
    ).count()

    return {

        "total_expenses":
            total_expenses,

        "paid_expenses":
            paid_expenses,

        "pending_count":
            pending_count,

        "approved_count":
            approved_count,

        "paid_count":
            paid_count,

        "count":
            expense_query.count()

    }


def _receivables_summary(
    db,
    merchant_id: str,
    branch_id: str | None = None
):

    receivable_query = _base_receivable_query(
        db,
        merchant_id,
        branch_id
    )

    outstanding = _safe_number(

        receivable_query.filter(
            ReceivableProjection.status
            == "OPEN"
        )

        .with_entities(
            func.sum(
                ReceivableProjection.balance
            )
        )

        .scalar()

    )

    total_original = _safe_number(

        receivable_query.with_entities(
            func.sum(
                ReceivableProjection.amount
            )
        ).scalar()

    )

    total_paid = _safe_number(

        receivable_query.with_entities(
            func.sum(
                ReceivableProjection.paid_amount
            )
        ).scalar()

    )

    open_count = receivable_query.filter(
        ReceivableProjection.status
        == "OPEN"
    ).count()

    settled_count = receivable_query.filter(
        ReceivableProjection.status
        == "SETTLED"
    ).count()

    return {

        "total_original":
            total_original,

        "total_paid":
            total_paid,

        "outstanding":
            outstanding,

        "open_count":
            open_count,

        "settled_count":
            settled_count,

        "count":
            receivable_query.count()

    }


def _payment_summary(
    db,
    merchant_id: str
):

    payment_query = _base_payment_query(
        db,
        merchant_id
    )

    completed_payments = _safe_number(

        payment_query.filter(
            PaymentProjection.status
            == "COMPLETED"
        )

        .with_entities(
            func.sum(
                PaymentProjection.amount
            )
        )

        .scalar()

    )

    pending_count = payment_query.filter(
        PaymentProjection.status
        == "PENDING"
    ).count()

    completed_count = payment_query.filter(
        PaymentProjection.status
        == "COMPLETED"
    ).count()

    failed_count = payment_query.filter(
        PaymentProjection.status
        == "FAILED"
    ).count()

    cancelled_count = payment_query.filter(
        PaymentProjection.status
        == "CANCELLED"
    ).count()

    return {

        "completed_payments":
            completed_payments,

        "pending_count":
            pending_count,

        "completed_count":
            completed_count,

        "failed_count":
            failed_count,

        "cancelled_count":
            cancelled_count,

        "count":
            payment_query.count()

    }


def _warnings(
    sales: dict,
    inventory: dict,
    receivables: dict,
    expenses: dict,
    payments: dict
):

    warnings = []

    if inventory[
        "low_stock_count"
    ] > 0:

        warnings.append(

            {

                "code":
                    "LOW_STOCK",

                "message":
                    f"{inventory['low_stock_count']} inventory item(s) are low in stock.",

                "severity":
                    "MEDIUM"

            }

        )

    if inventory[
        "negative_stock_count"
    ] > 0:

        warnings.append(

            {

                "code":
                    "NEGATIVE_STOCK",

                "message":
                    f"{inventory['negative_stock_count']} inventory item(s) have negative stock.",

                "severity":
                    "HIGH"

            }

        )

    if receivables[
        "outstanding"
    ] > sales[
        "total_sales_value"
    ] and receivables[
        "outstanding"
    ] > 0:

        warnings.append(

            {

                "code":
                    "HIGH_RECEIVABLES",

                "message":
                    "Outstanding receivables are higher than completed sales value.",

                "severity":
                    "HIGH"

            }

        )

    if payments[
        "failed_count"
    ] > 0:

        warnings.append(

            {

                "code":
                    "FAILED_PAYMENTS",

                "message":
                    f"{payments['failed_count']} payment(s) have failed.",

                "severity":
                    "MEDIUM"

            }

        )

    if expenses[
        "pending_count"
    ] > 0:

        warnings.append(

            {

                "code":
                    "PENDING_EXPENSES",

                "message":
                    f"{expenses['pending_count']} expense(s) are pending approval.",

                "severity":
                    "LOW"

            }

        )

    return warnings


def get_dashboard_summary(

    merchant_id: str,

    branch_id: str | None = None

):

    db = SessionLocal()

    try:

        sales = _sales_summary(
            db,
            merchant_id,
            branch_id
        )

        inventory = _inventory_summary(
            db,
            merchant_id,
            branch_id
        )

        expenses = _expense_summary(
            db,
            merchant_id,
            branch_id
        )

        receivables = _receivables_summary(
            db,
            merchant_id,
            branch_id
        )

        payments = _payment_summary(
            db,
            merchant_id
        )

        cashflow = {

            "completed_payments":
                payments[
                    "completed_payments"
                ],

            "paid_expenses":
                expenses[
                    "paid_expenses"
                ],

            "net_cash_indicator":
                payments[
                    "completed_payments"
                ]

                -

                expenses[
                    "paid_expenses"
                ]

        }

        warnings = _warnings(

            sales=sales,

            inventory=inventory,

            receivables=receivables,

            expenses=expenses,

            payments=payments

        )

        return {

            "merchant_id":
                merchant_id,

            "branch_id":
                branch_id,

            "sales":
                sales,

            "inventory":
                inventory,

            "cashflow":
                cashflow,

            "receivables":
                receivables,

            "expenses":
                expenses,

            "payments":
                payments,

            "warnings":
                warnings

        }

    finally:

        db.close()