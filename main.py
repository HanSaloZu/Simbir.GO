from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import Base, engine
from routers.account import router as AccountRouter
from routers.admin import account_router as AdminAccountRouter
from routers.admin import transport_router as AdminTransportRouter
from routers.payment import router as PaymentRouter
from routers.transport import router as TransportRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    debug=True, lifespan=lifespan, title="Simbir.GO API", docs_url="/ui-swagger"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    for err in errors:
        if "url" in err:
            err.pop("url")
        if "input" in err:
            err.pop("input")
        if "ctx" in err:
            err.pop("ctx")

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(errors),
    )


app.include_router(
    AccountRouter,
    tags=["AccountController"],
    prefix="/api/Account",
)

app.include_router(
    TransportRouter,
    tags=["TransportController"],
    prefix="/api/Transport",
)

app.include_router(
    PaymentRouter,
    tags=["PaymentController"],
    prefix="/api/Payment",
)

app.include_router(
    AdminAccountRouter,
    tags=["AdminAccountController"],
    prefix="/api/Admin/Account",
)

app.include_router(
    AdminTransportRouter,
    tags=["AdminTransportController"],
    prefix="/api/Admin/Transport",
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
