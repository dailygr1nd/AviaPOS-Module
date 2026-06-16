from fastapi import FastAPI

from api.routes.sales import router as sales_router
from api.routes.products import router as product_router
from api.routes.dashboard import router as dashboard_router

app = FastAPI(

    title="AviaPOS",

    version="0.1.0"

)

app.include_router(

    sales_router,

    prefix="/sales",

    tags=["Sales"]

)

app.include_router(

    product_router,

    prefix="/products",

    tags=["Products"]

)

app.include_router(

    dashboard_router,

    prefix="/dashboard",

    tags=["Dashboard"]

)


@app.get("/")

def health():

    return {

        "service": "AviaPOS",

        "status": "running"

    }