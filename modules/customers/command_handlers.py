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

from modules.customers.commands import (
    CreateCustomerCommand,
    DeactivateCustomerCommand,
    UpdateCustomerCommand
)

from modules.customers.models import (
    CustomerProjection
)


SUPPORTED_CUSTOMER_TYPES = {

    "REGULAR",

    "CREDIT",

    "BUSINESS",

    "SUPPLIER_CONTACT"

}


def _customer_aggregate_id(
    customer_id: str
) -> str:

    return f"customer:{customer_id}"


def _require_idempotency_key(
    idempotency_key: str | None
):

    if not idempotency_key:

        raise ValueError(
            "Idempotency-Key header is required."
        )


def _normalize_optional_text(
    value: str | None
):

    if value is None:

        return None

    value = value.strip()

    if not value:

        return None

    return value


def _normalize_email(
    value: str | None
):

    value = _normalize_optional_text(
        value
    )

    if value is None:

        return None

    return value.lower()


def _normalize_customer_type(
    value: str | None
):

    if value is None:

        return None

    normalized = value.strip().upper()

    if normalized not in SUPPORTED_CUSTOMER_TYPES:

        raise ValueError(

            f"Unsupported customer type: {value}"

        )

    return normalized


def _validate_credit_limit(
    value: float | None
):

    if value is not None and value < 0:

        raise ValueError(
            "Credit limit cannot be negative."
        )


def _ensure_contact_available(

    db,

    merchant_id: str,

    phone: str | None,

    email: str | None,

    customer_id: str | None = None

):

    if phone:

        query = (

            db.query(
                CustomerProjection
            )

            .filter(
                CustomerProjection.merchant_id
                == merchant_id,

                CustomerProjection.phone
                == phone

            )

        )

        if customer_id:

            query = query.filter(
                CustomerProjection.customer_id
                != customer_id
            )

        existing = query.first()

        if existing:

            raise ValueError(
                f"Phone already exists for this merchant: {phone}"
            )

    if email:

        query = (

            db.query(
                CustomerProjection
            )

            .filter(
                CustomerProjection.merchant_id
                == merchant_id,

                CustomerProjection.email
                == email

            )

        )

        if customer_id:

            query = query.filter(
                CustomerProjection.customer_id
                != customer_id
            )

        existing = query.first()

        if existing:

            raise ValueError(
                f"Email already exists for this merchant: {email}"
            )


class CreateCustomerCommandHandler:

    def handle(
        self,
        command: CreateCustomerCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if not command.name or not command.name.strip():

            raise ValueError(
                "Customer name is required."
            )

        _validate_credit_limit(
            command.credit_limit
        )

        customer_type = _normalize_customer_type(
            command.customer_type
        ) or "REGULAR"

        customer_id = (

            command.customer_id

            or

            str(
                uuid.uuid4()
            )

        )

        phone = _normalize_optional_text(
            command.phone
        )

        email = _normalize_email(
            command.email
        )

        address = _normalize_optional_text(
            command.address
        )

        tax_id = _normalize_optional_text(
            command.tax_id
        )

        name = command.name.strip()

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "customer_id":
                    customer_id,

                "name":
                    name,

                "phone":
                    phone,

                "email":
                    email,

                "address":
                    address,

                "customer_type":
                    customer_type,

                "tax_id":
                    tax_id,

                "credit_limit":
                    command.credit_limit

            }

        )

        aggregate_id = _customer_aggregate_id(
            customer_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "CreateCustomerCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            _ensure_contact_available(

                uow.db,

                command.merchant_id,

                phone,

                email

            )

            payload = {

                "customer_id":
                    customer_id,

                "merchant_id":
                    command.merchant_id,

                "name":
                    name,

                "phone":
                    phone,

                "email":
                    email,

                "address":
                    address,

                "customer_type":
                    customer_type,

                "tax_id":
                    tax_id,

                "credit_limit":
                    command.credit_limit

            }

            event = create_event(

                EventType.CUSTOMER_CREATED,

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

                "customer_id":
                    customer_id,

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


class UpdateCustomerCommandHandler:

    def handle(
        self,
        command: UpdateCustomerCommand
    ):

        _require_idempotency_key(
            command.idempotency_key
        )

        if command.expected_version < 1:

            raise ValueError(
                "Expected version must be at least 1."
            )

        _validate_credit_limit(
            command.credit_limit
        )

        changes = {}

        if command.name is not None:

            name = command.name.strip()

            if not name:

                raise ValueError(
                    "Customer name cannot be empty."
                )

            changes["name"] = name

        if command.phone is not None:

            changes["phone"] = _normalize_optional_text(
                command.phone
            )

        if command.email is not None:

            changes["email"] = _normalize_email(
                command.email
            )

        if command.address is not None:

            changes["address"] = _normalize_optional_text(
                command.address
            )

        if command.customer_type is not None:

            changes["customer_type"] = _normalize_customer_type(
                command.customer_type
            )

        if command.tax_id is not None:

            changes["tax_id"] = _normalize_optional_text(
                command.tax_id
            )

        if command.credit_limit is not None:

            changes["credit_limit"] = command.credit_limit

        if not changes:

            raise ValueError(
                "No customer changes provided."
            )

        request_hash = calculate_request_hash(

            {

                "merchant_id":
                    command.merchant_id,

                "customer_id":
                    command.customer_id,

                "expected_version":
                    command.expected_version,

                "changes":
                    changes

            }

        )

        aggregate_id = _customer_aggregate_id(
            command.customer_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "UpdateCustomerCommand",

                    request_hash=
                        request_hash

                )

            )

            if not is_new:

                return idempotency_record.response_payload

            _ensure_contact_available(

                uow.db,

                command.merchant_id,

                changes.get("phone"),

                changes.get("email"),

                customer_id=
                    command.customer_id

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

                "customer_id":
                    command.customer_id,

                "merchant_id":
                    command.merchant_id,

                **changes

            }

            event = create_event(

                EventType.CUSTOMER_UPDATED,

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

                "customer_id":
                    command.customer_id,

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


class DeactivateCustomerCommandHandler:

    def handle(
        self,
        command: DeactivateCustomerCommand
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

                "customer_id":
                    command.customer_id,

                "expected_version":
                    command.expected_version,

                "reason":
                    command.reason

            }

        )

        aggregate_id = _customer_aggregate_id(
            command.customer_id
        )

        with UnitOfWork() as uow:

            idempotency_record, is_new = (

                uow.idempotency.start(

                    merchant_id=
                        command.merchant_id,

                    idempotency_key=
                        command.idempotency_key,

                    command_name=
                        "DeactivateCustomerCommand",

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

                "customer_id":
                    command.customer_id,

                "merchant_id":
                    command.merchant_id,

                "active":
                    False,

                "reason":
                    command.reason

            }

            event = create_event(

                EventType.CUSTOMER_UPDATED,

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

                "customer_id":
                    command.customer_id,

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