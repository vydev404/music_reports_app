from typing import TypeVar, Generic

from pydantic import BaseModel

PS = TypeVar("PS", bound=BaseModel)

# PS - pydantic schema

class APIResponse(BaseModel, Generic[PS]):
    request_id: str
    code: int
    status: str
    message: str
    data: PS | None
