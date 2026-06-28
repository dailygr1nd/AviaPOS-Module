from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from modules.inventory.commands import (
    DeductInventoryCommand
)

from modules.payments.commands import (
    CompletePaymentCommand,
    CreatePaymentCommand
)

from modules.receivables.commands import (
    CreateReceivableCommand
)


class SaleCompletedReaction:

    def handle(
        self,
        event
    ):

        if event.event_type != "SALE_COMPLETED":

            return None

        register_command_handlers()

        payload = event.payload

        sale_id = payload[
            "sale_id"
        ]

        merchant_id = payload[
            "merchant_id"
        ]

        branch_id = payload[
            "branch_id"
        ]

        payment_method = payload[
            "payment_method"
        ]

        total = payload[
            "total"
        ]

        customer_id = payload.get(
            "customer_id"
        )

        items = payload.get(
            "items",
            []
        )

        inventory_results = self._deduct_inventory(

            sale_id=sale_id,

            merchant_id=merchant_id,

            branch_id=branch_id,

            items=items

        )

        financial_result = self._create_financial_record(

            sale_id=sale_id,

            merchant_id=merchant_id,

            branch_id=branch_id,

            payment_method=payment_method,

            total=total,

            customer_id=customer_id

        )

        return {

            "sale_id":
                sale_id,

            "inventory_results":
                inventory_results,

            "financial_result":
                financial_result

        }

    def _deduct_inventory(

        self,

        sale_id: str,

        merchant_id: str,

        branch_id: str,

        items: list

    ):

        results = []

        for index, item in enumerate(
            items
        ):

            expected_version = item.get(
                "inventory_expected_version"
            )

            if expected_version is None:

                raise ValueError(
                    "inventory_expected_version is required for every sale item."
                )

            result = command_bus.dispatch(

                DeductInventoryCommand(

                    merchant_id=merchant_id,

                    branch_id=branch_id,

                    product_id=item[
                        "product_id"
                    ],

                    sku=item[
                        "sku"
                    ],

                    quantity=item[
                        "quantity"
                    ],

                    reason=f"SALE:{sale_id}",

                    expected_version=expected_version,

                    idempotency_key=f"{sale_id}:inventory:{index}"

                )

            )

            results.append(
                result
            )

        return results

    def _create_financial_record(

        self,

        sale_id: str,

        merchant_id: str,

        branch_id: str,

        payment_method: str,

        total: float,

        customer_id: str | None

    ):

        if payment_method == "CREDIT":

            if not customer_id:

                raise ValueError(
                    "Credit sale requires customer_id."
                )

            return command_bus.dispatch(

                CreateReceivableCommand(

                    merchant_id=merchant_id,

                    branch_id=branch_id,

                    customer_id=customer_id,

                    sale_id=sale_id,

                    amount=total,

                    idempotency_key=f"{sale_id}:receivable:create"

                )

            )

        payment_response = command_bus.dispatch(

            CreatePaymentCommand(

                merchant_id=merchant_id,

                amount=total,

                payment_method=payment_method,

                reference_type="SALE",

                reference_id=sale_id,

                notes="Payment created from completed sale.",

                idempotency_key=f"{sale_id}:payment:create"

            )

        )

        payment_id = payment_response[
            "payment_id"
        ]

        completion_response = command_bus.dispatch(

            CompletePaymentCommand(

                merchant_id=merchant_id,

                payment_id=payment_id,

                expected_version=1,

                idempotency_key=f"{sale_id}:payment:complete"

            )

        )

        return {

            "created":
                payment_response,

            "completed":
                completion_response

        }