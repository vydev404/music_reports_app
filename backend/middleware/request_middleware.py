import logging
import uuid

from fastapi import Request
from starlette.responses import Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logging.info(f"Request ID: {request_id} | {request.method} {request.url}")
    return response