from projections.sales_projection import (
    SalesProjection
)

events = [

    {
        "event_type":
            "SALE_CREATED",

        "payload": {

            "amount": 100
        }
    },

    {
        "event_type":
            "SALE_CREATED",

        "payload": {

            "amount": 50
        }
    }

]

projection = (
    SalesProjection()
)

projection.replay(events)

print(
    projection.total()
)