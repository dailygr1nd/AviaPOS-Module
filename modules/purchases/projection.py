purchases = {}


def apply_event(event):
    raise RuntimeError(
        "modules.purchases.projection.apply_event is deprecated. "
        "Use modules.purchases.projector.PurchaseProjector instead."
    )