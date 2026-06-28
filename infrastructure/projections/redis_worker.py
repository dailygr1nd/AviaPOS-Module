import json

from types import SimpleNamespace

from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.redis.client import (
    redis_client
)

from infrastructure.redis.consumer import (
    CONSUMER_NAME,
    EVENT_STREAM,
    GROUP_NAME
)

from modules.branches.projector import (
    BranchProjector
)

from modules.customers.projector import (
    CustomerProjector
)

from modules.expenses.projector import (
    ExpenseProjector
)

from modules.inventory.projector import (
    InventoryProjector
)

from modules.payments.projector import (
    PaymentProjector
)

from modules.products.projector import (
    ProductProjector
)

from modules.receivables.projector import (
    ReceivableProjector
)

from modules.sales.projector import (
    SalesProjector
)


def _build_event(
    data: dict
):

    return SimpleNamespace(

        persisted_event_id=data.get(
            "persisted_event_id"
        ),

        event_id=data.get(
            "event_id"
        ),

        event_type=data.get(
            "event_type"
        ),

        merchant_id=data.get(
            "merchant_id"
        ),

        aggregate_id=data.get(
            "aggregate_id"
        ),

        version=int(
            data.get(
                "version",
                1
            )
        ),

        previous_hash=data.get(
            "previous_hash"
        ),

        current_hash=data.get(
            "current_hash"
        ),

        payload=json.loads(
            data.get(
                "payload",
                "{}"
            )
        )

    )


def _build_projectors(
    db
):

    return [

        BranchProjector(
            db
        ),

        ProductProjector(
            db
        ),

        CustomerProjector(
            db
        ),

        InventoryProjector(
            db
        ),

        ExpenseProjector(
            db
        ),

        PaymentProjector(
            db
        ),

        ReceivableProjector(
            db
        ),

        SalesProjector(
            db
        )

    ]


def start_projection_worker():

    db = SessionLocal()

    projectors = _build_projectors(
        db
    )

    while True:

        messages = redis_client.xreadgroup(

            GROUP_NAME,

            CONSUMER_NAME,

            {
                EVENT_STREAM: ">"
            },

            count=10,

            block=5000

        )

        if not messages:

            continue

        for _, records in messages:

            for msg_id, data in records:

                event = _build_event(
                    data
                )

                try:

                    for projector in projectors:

                        projector.handle(
                            event
                        )

                    redis_client.xack(

                        EVENT_STREAM,

                        GROUP_NAME,

                        msg_id

                    )

                except Exception as exc:

                    db.rollback()

                    print(
                        f"Projection failed for {event.event_id}: {exc}"
                    )