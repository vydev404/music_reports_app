from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from core.models import db_manager
from middleware.request_middleware import request_id_middleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await db_manager.create_tables()
    yield
    await db_manager.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(
    api_router,
)
origins = [
    "http://localhost:5173",  # Vite/React
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_id_middleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
