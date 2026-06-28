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

from modules.products.commands import (
    CreateProductCommand,
    DeactivateProductCommand,
    UpdateProductCommand
)

from modules.products.models import (
    ProductProjection
)


def _product_aggregate_id(
    product_id: str
) -> str:

    return f"product:{product_id}"


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


def _normalize_sku(
    sku: str
) -> str:

    return sku.strip().upper()


def _validate_prices(

    selling_price: float | None,

    cost_price: float | None

):

    if selling_price is not None and selling_price < 0:

        raise ValueError(
            "Selling price cannot be negative."
        )

    if cost_price is not None and cost_price < 0:

        raise ValueError(
            "Cost price cannot be negative."
        )


def _ensure_sku_available(

    db,

    merchant_id: str,

    sku: str,

    product_id: str | None = None

):

    query = (

        db.query(
            ProductProjection
        )

        .filter(
            ProductProjection.merchant_id
            == merchant_id,

            ProductProjection.sku
            == sku

        )

    )

    if product_id:

        query = query.filter(
            ProductProjection.product_id
            != product_id
        )

    existing = query.first()

    if existing:

        raise ValueError(
            f"SKU already exists for this merchant: {sku}"
        )


class CreateProductCommandHandler:

    def handle(
        self,
        command: CreateProductCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.name or not command.name.strip():

            raise ValueError(
                "Product name is required."
            )

        if not command.sku or not command.sku.strip():

            raise ValueError(
                "SKU is required."
            )

        _validate_prices(

            command.selling_price,

            command.cost_price

        )

        product_id = (

            command.product_id

            or

            str(
                uuid.uuid4()
            )

        )

        sku = _normalize_sku(
            command.sku
        )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "product_id":
                    product_id,

                "sku":
                    sku,

                "name":
                    command.name.strip(),

                "selling_price":
                    command.selling_price,

                "cost_price":
                    command.cost_price,

                "category":
                    command.category,

                "barcode":
                    command.barcode

            }

        )

        aggregate_id = _product_aggregate_id(
            product_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "CreateProductCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            _ensure_sku_available(

                uow.db,

                command.merchant_id,

                sku

            )

            payload = {

                "product_id":
                    product_id,

                "merchant_id":
                    command.merchant_id,

                "sku":
                    sku,

                "name":
                    command.name.strip(),

                "selling_price":
                    command.selling_price,

                "cost_price":
                    command.cost_price,

                "category":
                    command.category,

                "barcode":
                    command.barcode

            }

            event = create_event(

                EventType.PRODUCT_CREATED,

                command.merchant_id,

                payload,

                previous_hash=
                    uow.events.get_latest_hash(
                        command.merchant_id
                    ),

                aggregate_id=
                    aggregate_id,

                version=1,

                metadata={

                    "idempotency_key":
                        command.idempotency_key

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

                "success":
                    True,

                "product_id":
                    product_id,

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


class UpdateProductCommandHandler:

    def handle(
        self,
        command: UpdateProductCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        _validate_prices(

            command.selling_price,

            command.cost_price

        )

        normalized_sku = None

        if command.sku:

            normalized_sku = _normalize_sku(
                command.sku
            )

        changes = {}

        for key, value in {

            "sku":
                normalized_sku,

            "name":
                command.name.strip()
                if command.name
                else None,

            "selling_price":
                command.selling_price,

            "cost_price":
                command.cost_price,

            "category":
                command.category,

            "barcode":
                command.barcode

        }.items():

            if value is not None:

                changes[key] = value

        if not changes:

            raise ValueError(
                "No product changes provided."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "product_id":
                    command.product_id,

                "expected_version":
                    command.expected_version,

                "changes":
                    changes

            }

        )

        aggregate_id = _product_aggregate_id(
            command.product_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "UpdateProductCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            if normalized_sku:

                _ensure_sku_available(

                    uow.db,

                    command.merchant_id,

                    normalized_sku,

                    product_id=
                        command.product_id

                )

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

                "product_id":
                    command.product_id,

                "merchant_id":
                    command.merchant_id,

                **changes

            }

            event = create_event(

                EventType.PRODUCT_UPDATED,

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

                "success":
                    True,

                "product_id":
                    command.product_id,

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


class DeactivateProductCommandHandler:

    def handle(
        self,
        command: DeactivateProductCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "product_id":
                    command.product_id,

                "expected_version":
                    command.expected_version,

                "reason":
                    command.reason

            }

        )

        aggregate_id = _product_aggregate_id(
            command.product_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "DeactivateProductCommand",

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

                "product_id":
                    command.product_id,

                "merchant_id":
                    command.merchant_id,

                "active":
                    False,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.PRODUCT_UPDATED,

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

                "success":
                    True,

                "product_id":
                    command.product_id,

                "event_id":
                    event.event_id,

                "event_type":
                    event.event_type,

                "version":
                    event.version,

                "active":
                    False

            }

            uow.idempotency.complete(

                idempotency_record,

                response

            )

            return response