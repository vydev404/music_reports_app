from typing import TypeVar, Generic
from fastapi import Request

from pydantic import BaseModel

PS = TypeVar("PS", bound=BaseModel)

# PS - pydantic schema

class APIResponse(BaseModel, Generic[PS]):
    request_id: str
    message: str| None = None
    data: PS | None = None


def format_response(request: Request, data, message="Success"):
    return APIResponse(
        request_id=request.state.request_id,
        message=message,
        data=data
    )