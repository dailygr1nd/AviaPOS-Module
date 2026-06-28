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

from modules.inventory.commands import (
    AdjustInventoryCommand,
    DeductInventoryCommand,
    ReceiveInventoryCommand
)


def _inventory_aggregate_id(

    branch_id: str,

    product_id: str

) -> str:

    return f"inventory:{branch_id}:{product_id}"


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


def _calculate_stock_from_events(
    events
) -> int:

    quantity = 0

    for event in events:

        if event.event_type == "INVENTORY_RECEIVED":

            quantity += event.payload[
                "quantity"
            ]

        elif event.event_type == "INVENTORY_DEDUCTED":

            quantity -= event.payload[
                "quantity"
            ]

        elif event.event_type == "INVENTORY_ADJUSTED":

            quantity += event.payload[
                "adjustment"
            ]

    return quantity


def _current_stock(

    uow,

    merchant_id: str,

    aggregate_id: str

) -> int:

    events = uow.events.get_by_aggregate_ordered(

        merchant_id,

        aggregate_id

    )

    return _calculate_stock_from_events(
        events
    )


class ReceiveInventoryCommandHandler:

    def handle(
        self,
        command: ReceiveInventoryCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.quantity <= 0:

            raise ValueError(
                "Received quantity must be positive."
            )

        if command.cost_price < 0:

            raise ValueError(
                "Cost price cannot be negative."
            )

        if command.expected_version < 0:

            raise ValueError(
                "Expected version cannot be negative."
            )

        aggregate_id = _inventory_aggregate_id(

            command.branch_id,

            command.product_id

        )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "quantity":
                    command.quantity,

                "cost_price":
                    command.cost_price,

                "expected_version":
                    command.expected_version

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
                        "ReceiveInventoryCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            current_version = uow.events.assert_expected_version(

                merchant_id=
                    command.merchant_id,

                aggregate_id=
                    aggregate_id,

                expected_version=
                    command.expected_version

            )

            next_version = current_version + 1

            payload = {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "quantity":
                    command.quantity,

                "cost_price":
                    command.cost_price

            }

            event = create_event(

                EventType.INVENTORY_RECEIVED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    aggregate_id,

                version=
                    next_version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key,

                    "expected_version":
                        command.expected_version

                }

            )

            persisted_event = uow.events.append(

                event,

                commit=False

            )

            uow.outbox.add_event(

                event,

                persisted_event_id=
                    persisted_event.id

            )

            response = {

                "success": True,

                "aggregate_id":
                    aggregate_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response


class DeductInventoryCommandHandler:

    def handle(
        self,
        command: DeductInventoryCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.quantity <= 0:

            raise ValueError(
                "Deducted quantity must be positive."
            )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        aggregate_id = _inventory_aggregate_id(

            command.branch_id,

            command.product_id

        )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "quantity":
                    command.quantity,

                "reason":
                    command.reason,

                "expected_version":
                    command.expected_version

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
                        "DeductInventoryCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            current_version = uow.events.assert_expected_version(

                merchant_id=
                    command.merchant_id,

                aggregate_id=
                    aggregate_id,

                expected_version=
                    command.expected_version

            )

            available_stock = _current_stock(

                uow,

                command.merchant_id,

                aggregate_id

            )

            if command.quantity > available_stock:

                raise ValueError(

                    f"Insufficient stock. Available={available_stock}, "

                    f"requested={command.quantity}."

                )

            next_version = current_version + 1

            payload = {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "quantity":
                    command.quantity,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.INVENTORY_DEDUCTED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    aggregate_id,

                version=
                    next_version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key,

                    "expected_version":
                        command.expected_version

                }

            )

            persisted_event = uow.events.append(

                event,

                commit=False

            )

            uow.outbox.add_event(

                event,

                persisted_event_id=
                    persisted_event.id

            )

            response = {

                "success": True,

                "aggregate_id":
                    aggregate_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version,

                "remaining_stock":
                    available_stock - command.quantity

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response


class AdjustInventoryCommandHandler:

    def handle(
        self,
        command: AdjustInventoryCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.adjustment == 0:

            raise ValueError(
                "Adjustment cannot be zero."
            )

        if command.expected_version < 0:

            raise ValueError(
                "Expected version cannot be negative."
            )

        aggregate_id = _inventory_aggregate_id(

            command.branch_id,

            command.product_id

        )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "adjustment":
                    command.adjustment,

                "reason":
                    command.reason,

                "expected_version":
                    command.expected_version

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
                        "AdjustInventoryCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            current_version = uow.events.assert_expected_version(

                merchant_id=
                    command.merchant_id,

                aggregate_id=
                    aggregate_id,

                expected_version=
                    command.expected_version

            )

            available_stock = _current_stock(

                uow,

                command.merchant_id,

                aggregate_id

            )

            resulting_stock = (

                available_stock

                +

                command.adjustment

            )

            if resulting_stock < 0:

                raise ValueError(

                    f"Adjustment would create negative stock. "

                    f"Available={available_stock}, "

                    f"adjustment={command.adjustment}."

                )

            next_version = current_version + 1

            payload = {

                "merchant_id":
                    command.merchant_id,

                "branch_id":
                    command.branch_id,

                "product_id":
                    command.product_id,

                "sku":
                    command.sku,

                "adjustment":
                    command.adjustment,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.INVENTORY_ADJUSTED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    aggregate_id,

                version=
                    next_version,

                metadata={

                    "idempotency_key":
                        command.idempotency_key,

                    "expected_version":
                        command.expected_version

                }

            )

            persisted_event = uow.events.append(

                event,

                commit=False

            )

            uow.outbox.add_event(

                event,

                persisted_event_id=
                    persisted_event.id

            )

            response = {

                "success": True,

                "aggregate_id":
                    aggregate_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version,

                "quantity":
                    resulting_stock

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response