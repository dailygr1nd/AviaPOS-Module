import uuid

from core.events.types import EventType

from core.ledger.event_factory import (
    create_event
)

from core.ledger.store import (
    append_event
)

from core.ledger.hash_chain import (
    get_last_event_hash
)

from modules.sales.aggregate import (
    SaleAggregate
)

from modules.inventory.service import (
    deduct_stock
)

from modules.debts.service import (
    create_debt
)


SUPPORTED_PAYMENT_METHODS = {

    "CASH",

    "MOBILE_MONEY",

    "BANK",

    "CREDIT"

}


def create_sale(

    merchant_id: str,

    items: list,

    payment_method: str,

    customer_id: str = None

):

    if payment_method not in (
        SUPPORTED_PAYMENT_METHODS
    ):

        raise ValueError(
            f"Unsupported payment method: "
            f"{payment_method}"
        )

    sale_id = str(
        uuid.uuid4()
    )

    aggregate = SaleAggregate()

    sale_event = create_event(

        EventType.SALE_CREATED,

        merchant_id,

        {
            "sale_id": sale_id,
            "customer_id": customer_id
        },

        get_last_event_hash()

    )

    append_event(
        sale_event
    )

    for item in items:

        line = aggregate.add_line(

            product_id=item[
                "product_id"
            ],

            sku=item[
                "sku"
            ],

            quantity=item[
                "quantity"
            ],

            unit_price=item[
                "unit_price"
            ]

        )

        line_event = create_event(

            EventType.SALE_LINE_ADDED,

            merchant_id,

            {

                "sale_id":
                    sale_id,

                "product_id":
                    line.product_id,

                "sku":
                    line.sku,

                "quantity":
                    line.quantity,

                "unit_price":
                    line.unit_price,

                "line_total":
                    line.line_total

            },

            get_last_event_hash()

        )

        append_event(
            line_event
        )

        deduct_stock(

            merchant_id=
                merchant_id,

            product_id=
                line.product_id,

            sku=
                line.sku,

            quantity=
                line.quantity,

            reason=
                "SALE"

        )

    if payment_method == "CREDIT":

        if not customer_id:

            raise ValueError(
                "Credit sales require customer_id"
            )

        debt_id = str(
            uuid.uuid4()
        )

        create_debt(

            merchant_id=
                merchant_id,

            debt_id=
                debt_id,

            customer_id=
                customer_id,

            sale_id=
                sale_id,

            amount=
                aggregate.total

        )

    else:

        payment_event = create_event(

            EventType.PAYMENT_RECEIVED,

            merchant_id,

            {

                "sale_id":
                    sale_id,

                "amount":
                    aggregate.total,

                "method":
                    payment_method

            },

            get_last_event_hash()

        )

        append_event(
            payment_event
        )

    completion_event = create_event(

        EventType.SALE_COMPLETED,

        merchant_id,

        {

            "sale_id":
                sale_id,

            "total":
                aggregate.total

        },

        get_last_event_hash()

    )

    append_event(
        completion_event
    )

    return {

        "sale_id":
            sale_id,

        "total":
            aggregate.total,

        "payment_method":
            payment_method

    }