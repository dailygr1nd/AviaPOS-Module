from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from modules.payments.commands import (
    CompletePaymentCommand,
    CreatePaymentCommand
)


class PaymentCaptureMatchedReaction:
    def handle(self, event):
        if event.event_type not in {
            "PAYMENT_CAPTURE_RECEIVED",
            "PAYMENT_CAPTURE_MATCHED"
        }:
            return None

        payload = event.payload

        reference_type = payload.get("reference_type")
        reference_id = payload.get("reference_id")

        if not reference_type or not reference_id:
            return None

        register_command_handlers()

        capture_id = payload["capture_id"]
        merchant_id = payload["merchant_id"]

        create_result = command_bus.dispatch(
            CreatePaymentCommand(
                merchant_id=merchant_id,
                amount=payload["amount"],
                payment_method=payload["payment_method"],
                reference_type=reference_type,
                reference_id=reference_id,
                notes=(
                    f"Captured via {payload['provider']} "
                    f"{payload['provider_reference']}"
                ),
                idempotency_key=(
                    f"{capture_id}:payment-create"
                )
            )
        )

        payment_id = create_result.get("payment_id")

        complete_result = command_bus.dispatch(
            CompletePaymentCommand(
                merchant_id=merchant_id,
                payment_id=payment_id,
                expected_version=1,
                idempotency_key=(
                    f"{capture_id}:payment-complete"
                )
            )
        )

        return {
            "capture_id": capture_id,
            "payment_id": payment_id,
            "create_result": create_result,
            "complete_result": complete_result
        }