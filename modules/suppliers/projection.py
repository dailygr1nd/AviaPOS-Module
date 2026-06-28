suppliers = {}


def apply_event(event):
    raise RuntimeError(
        "modules.suppliers.projection.apply_event is deprecated. "
        "Use modules.suppliers.projector.SupplierProjector instead."
    )