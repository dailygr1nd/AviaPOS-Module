from fastapi import FastAPI

from api.routes.products import router as product_router
from api.routes.inventory import router as inventory_router
from api.routes.sales import router as sales_router
from api.routes.debts import router as debt_router


app = FastAPI(

    title="AviaPOS",

    version="0.1.0"
)


app.include_router(
    product_router
)

app.include_router(
    inventory_router
)

app.include_router(
    sales_router
)

app.include_router(
    debt_router
)