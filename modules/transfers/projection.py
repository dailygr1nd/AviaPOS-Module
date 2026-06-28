transfers = {}


def apply_event(event):
    raise RuntimeError(
        "modules.transfers.projection.apply_event is deprecated. "
        "Use modules.transfers.projector.TransferProjector instead."
    )