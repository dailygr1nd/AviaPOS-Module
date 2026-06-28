branches = {}


def apply_event(event):
    raise RuntimeError(
        "modules.branches.projection.apply_event is deprecated. "
        "Use modules.branches.projector.BranchProjector instead."
    )