from modules.payment_capture.adapters.base import (
    NormalizedPaymentCapture,
    PaymentCaptureAdapter
)


class MpesaPaymentCaptureAdapter(PaymentCaptureAdapter):
    provider = "MPESA"

    def normalize(
        self,
        payload: dict
    ) -> NormalizedPaymentCapture:
        provider_reference = (
            payload.get("TransID")
            or payload.get("transaction_id")
            or payload.get("provider_reference")
        )

        if not provider_reference:
            raise ValueError(
                "M-PESA payload missing provider reference."
            )

        amount = (
            payload.get("TransAmount")
            or payload.get("amount")
        )

        if amount is None:
            raise ValueError(
                "M-PESA payload missing amount."
            )

        payer_reference = (
            payload.get("MSISDN")
            or payload.get("payer_reference")
            or payload.get("phone")
        )

        payer_name = (
            payload.get("FirstName")
            or payload.get("payer_name")
        )

        bill_ref = (
            payload.get("BillRefNumber")
            or payload.get("business_short_code")
            or payload.get("external_reference")
        )

        channel = (
            payload.get("provider_channel")
            or payload.get("channel")
            or "MPESA_PAYBILL"
        )

        return NormalizedPaymentCapture(
            provider="MPESA",
            provider_channel=str(channel).upper(),
            provider_reference=str(provider_reference),
            external_reference=str(bill_ref) if bill_ref else None,
            payer_reference=str(payer_reference) if payer_reference else None,
            payer_name=str(payer_name) if payer_name else None,
            amount=float(amount),
            currency=str(
                payload.get("currency", "KES")
            ).upper(),
            payment_method="MOBILE_MONEY",
            raw_payload=payload
        )