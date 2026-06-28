import uuid

from core.events.types import (
    EventType
)

from core.ledger.event_factory import (
    create_event
)

from infrastructure.database.unit_of_work import (
    UnitOfWork
)

from infrastructure.idempotency.request_hash import (
    calculate_request_hash
)

from modules.sales.commands import (
    CreateSaleCommand
)


SUPPORTED_PAYMENT_METHODS = {

    "CASH",

    "MOBILE_MONEY",

    "BANK",

    "CARD",

    "CREDIT"

}


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


def _sale_aggregate_id(
    sale_id: str
) -> str:

    return f"sale:{sale_id}"


def _line_total(

    quantity: int,

    unit_price: float

) -> float:

    return quantity * unit_price


class CreateSaleCommandHandler:

    def handle(
        self,
        command: CreateSaleCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.items:

            raise ValueError(
                "Sale must contain at least one item."
            )

        if command.payment_method not in SUPPORTED_PAYMENT_METHODS:

            raise ValueError(

                f"Unsupported payment method: {command.payment_method}"

            )

        if command.payment_method == "CREDIT" and not command.customer_id:

            raise ValueError(
                "Credit sales require customer_id."
            )

        normalized_items = []

        total = 0

        for item in command.items:

            if item.quantity <= 0:

                raise ValueError(
                    "Sale item quantity must be positive."
                )

            if item.unit_price <= 0:

                raise ValueError(
                    "Sale item unit price must be positive."
                )

            if item.inventory_expected_version < 1:

                raise ValueError(
                    "Sale item inventory_expected_version must be at least 1."
                )

            line_total = _line_total(

                item.quantity,

                item.unit_price

            )

            total += line_total

            normalized_items.append(

                {

                    "product_id":
                        item.product_id,

                    "sku":
                        item.sku,

                    "quantity":
                        item.quantity,

                    "unit_price":
                        item.unit_price,

                    "line_total":
                        line_total,

                    "inventory_expected_version":
                        item.inventory_expected_version

                }

            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "items":
                    normalized_items,

                "payment_method":
                    command.payment_method,

                "customer_id":
                    command.customer_id

            }

        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "CreateSaleCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            sale_id = str(
                uuid.uuid4()
            )

            aggregate_id = _sale_aggregate_id(
                sale_id
            )

            version = 1

            sale_created_payload = {

                "sale_id":
                    sale_id,

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "customer_id":
                    command.customer_id,

                "payment_method":
                    command.payment_method

            }

            sale_created_event = create_event(

                EventType.SALE_CREATED,

                command.merchant_id,

                sale_created_payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    aggregate_id,

                version=
                    version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key

                }

            )

            persisted_created = uow.events.append(

                sale_created_event,

                commit=False

            )

            uow.outbox.add_event(

                sale_created_event,

                persisted_event_id=
                    persisted_created.id

            )

            last_event_hash = sale_created_event.current_hash

            for item in normalized_items:

                version += 1

                line_payload = {

                    "sale_id":
                        sale_id,

                    "merchant_id":
                        command.merchant_id,

                    "branch_id":
                        command.branch_id,

                    "product_id":
                        item["product_id"],

                    "sku":
                        item["sku"],

                    "quantity":
                        item["quantity"],

                    "unit_price":
                        item["unit_price"],

                    "line_total":
                        item["line_total"],

                    "inventory_expected_version":
                        item[
                            "inventory_expected_version"
                        ]

                }

                line_event = create_event(

                    EventType.SALE_LINE_ADDED,

                    command.merchant_id,

                    line_payload,

                    previous_hash=
                        last_event_hash,

                    aggregate_id=
                        aggregate_id,

                    version=
                        version,

                    metadata={

                        "idempotency_key":
                            command.idempotency_key

                    }

                )

                persisted_line = uow.events.append(

                    line_event,

                    commit=False

                )

                uow.outbox.add_event(

                    line_event,

                    persisted_event_id=
                        persisted_line.id

                )

                last_event_hash = line_event.current_hash

            version += 1

            completed_payload = {

                "sale_id":
                    sale_id,

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "total":
                    total,

                "payment_method":
                    command.payment_method,

                "customer_id":
                    command.customer_id,

                "items":
                    normalized_items

            }

            completed_event = create_event(

                EventType.SALE_COMPLETED,

                command.merchant_id,

                completed_payload,

                previous_hash=
                    last_event_hash,

                aggregate_id=
                    aggregate_id,

                version=
                    version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key

                }

            )

            persisted_completed = uow.events.append(

                completed_event,

                commit=False

            )

            uow.outbox.add_event(

                completed_event,

                persisted_event_id=
                    persisted_completed.id

            )

            response = {

                "success": True,

                "sale_id":
                    sale_id,

                "total":
                    total,

                "payment_method":
                    command.payment_method,

                "event_id":
                    completed_event.event_id,

                "event_type":
                    completed_event.event_type,

                "version":
                    completed_event.version

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response