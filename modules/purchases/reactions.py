from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from modules.inventory.commands import ReceiveInventoryCommand


class PurchaseReceivedReaction:
    def handle(self, event):
        if event.event_type != "PURCHASE_RECEIVED":
            return None

        register_command_handlers()

        payload = event.payload

        purchase_id = payload["purchase_id"]
        merchant_id = payload["merchant_id"]
        branch_id = payload["branch_id"]
        items = payload.get("items", [])

        results = []

        for index, item in enumerate(items):
            result = command_bus.dispatch(
                ReceiveInventoryCommand(
                    merchant_id=merchant_id,
                    branch_id=branch_id,
                    product_id=item["product_id"],
                    sku=item["sku"],
                    quantity=item["quantity"],
                    cost_price=item["cost_price"],
                    expected_version=item["inventory_expected_version"],
                    idempotency_key=f"{purchase_id}:inventory-receive:{index}"
                )
            )

            results.append(result)

        return {
            "purchase_id": purchase_id,
            "inventory_results": results
        }