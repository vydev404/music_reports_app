from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_manager
from api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await db_manager.create_tables()
    yield
    await db_manager.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(
    api_router,
    prefix="/"
)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)