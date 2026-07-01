from modules.payment_capture.adapters.mpesa import (
    MpesaPaymentCaptureAdapter
)


class PaymentCaptureAdapterRegistry:
    def __init__(self):
        self.adapters = {
            "MPESA": MpesaPaymentCaptureAdapter()
        }

    def get(
        self,
        provider: str
    ):
        key = provider.strip().upper()

        adapter = self.adapters.get(key)

        if not adapter:
            raise ValueError(
                f"No payment capture adapter registered for provider: {provider}"
            )

        return adapter


adapter_registry = PaymentCaptureAdapterRegistry()