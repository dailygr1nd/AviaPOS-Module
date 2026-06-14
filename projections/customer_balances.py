from collections import defaultdict

from projections.base import (
    Projection
)


class CustomerBalances(
    Projection
):

    def __init__(self):

        self.balances = (
            defaultdict(float)
        )

def apply(
    self,
    event
):

    payload = event.payload

    if (
        event.event_type
        == "DEBT_CREATED"
    ):

        self.balances[
            payload["customer_id"]
        ] += payload["amount"]

    elif (
        event.event_type
        == "DEBT_SETTLED"
    ):

        self.balances[
            payload["customer_id"]
        ] -= payload["amount"]