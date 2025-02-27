from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware

from api.routes import router as api_router
from core.models import db_manager
from middleware.request_middleware import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await db_manager.create_tables()
    yield
    await db_manager.dispose()


app = FastAPI(lifespan=lifespan,
              middleware=[Middleware(RequestIDMiddleware)])
app.include_router(
    api_router,
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)