from core.commands.registry import (
    command_bus,
    register_command_handlers
)

from modules.inventory.commands import (
    DeductInventoryCommand,
    ReceiveInventoryCommand
)


class StockTransferDispatchedReaction:
    def handle(self, event):
        if event.event_type != "TRANSFER_DISPATCHED":
            return None

        register_command_handlers()

        payload = event.payload

        transfer_id = payload["transfer_id"]
        merchant_id = payload["merchant_id"]
        source_branch_id = payload["source_branch_id"]
        items = payload.get("items", [])

        results = []

        for index, item in enumerate(items):
            result = command_bus.dispatch(
                DeductInventoryCommand(
                    merchant_id=merchant_id,
                    branch_id=source_branch_id,
                    product_id=item["product_id"],
                    sku=item["sku"],
                    quantity=item["quantity"],
                    reason="STOCK_TRANSFER_DISPATCH",
                    expected_version=item[
                        "source_inventory_expected_version"
                    ],
                    idempotency_key=(
                        f"{transfer_id}:stock-dispatch-deduct:{index}"
                    )
                )
            )

            results.append(result)

        return {
            "transfer_id": transfer_id,
            "source_inventory_results": results
        }


class StockTransferReceivedReaction:
    def handle(self, event):
        if event.event_type != "TRANSFER_RECEIVED":
            return None

        register_command_handlers()

        payload = event.payload

        transfer_id = payload["transfer_id"]
        merchant_id = payload["merchant_id"]
        destination_branch_id = payload["destination_branch_id"]
        items = payload.get("items", [])

        results = []

        for index, item in enumerate(items):
            result = command_bus.dispatch(
                ReceiveInventoryCommand(
                    merchant_id=merchant_id,
                    branch_id=destination_branch_id,
                    product_id=item["product_id"],
                    sku=item["sku"],
                    quantity=item["quantity"],
                    cost_price=item["cost_price"],
                    expected_version=item[
                        "destination_inventory_expected_version"
                    ],
                    idempotency_key=(
                        f"{transfer_id}:stock-receive:{index}"
                    )
                )
            )

            results.append(result)

        return {
            "transfer_id": transfer_id,
            "destination_inventory_results": results
        }