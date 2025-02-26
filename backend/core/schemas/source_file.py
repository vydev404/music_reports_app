from dataclasses import field
from uuid import UUID

from pydantic import BaseModel


class SourceFileBase(BaseModel):
    name: str
    full_name: str
    path: str
    hash: str
    type: str


class SourceFileCreate(SourceFileBase):
    pass


class SourceFileUpdate(BaseModel):
    path: str | None = None
    hash: str | None = None
    file_data: dict | None = None
    status: str | None = None
    error_stage: str | None = None
    error_message: str | None = None


class SourceFileResponse(SourceFileBase):
    id: UUID
    status: str
    error_stage: str | None = None
    error_message: str | None = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class SourceFileResponseList(BaseModel):
    files: list[SourceFileResponse] = field(default_factory=list)

class SourceFileDelete(BaseModel):
    id: UUID
    deleted: bool
