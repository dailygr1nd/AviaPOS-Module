def create_purchase(*args, **kwargs):
    raise RuntimeError(
        "modules.purchases.service.create_purchase is deprecated. "
        "Use modules.purchases.api with CreatePurchaseCommand instead."
    )