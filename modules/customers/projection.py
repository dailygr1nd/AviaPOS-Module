customers = {}


def apply_event(
    event
):

    raise RuntimeError(

        "modules.customers.projection.apply_event is deprecated. "

        "Use modules.customers.projector.CustomerProjector instead."

    )