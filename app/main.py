from fastapi import FastAPI

from .database import database, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="meterite",
    description="""
    Meterite is a sink for timebased metrics
    - Create metrics
    - Add meter reading to each metric
    - If reading timestamp is not given, use system time
    - You can truncate the meter readings to 5th minute, hour, week etc.
    - Keep current and last reading info handy at metric level
    - Meters are grouped by orgs and authentication keys are tied to orgs.
    """,
    version="1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# ------------ routers -----------------------------
from .routers import docs, metrics, meters

app.include_router(
    docs.router, tags=["docs"], responses={404: {"description": "Not found"}}
)

app.include_router(
    metrics.router,
    prefix="/metric",
    tags=["metric"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    meters.router,
    prefix="/metric",
    tags=["meter"],
    responses={404: {"description": "Not found"}},
)
