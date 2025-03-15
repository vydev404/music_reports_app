from dataclasses import field
from datetime import datetime
from pydantic import BaseModel


class SourceFileBase(BaseModel):
    path: str
    full_name: str
    name: str
    type: str
    hash: str | None = None


class SourceFileCreate(BaseModel):
    path: str


class SourceFileUpdate(BaseModel):

    path: str | None = None
    name: str | None = None
    hash: str | None = None
    file_data: dict | None = None


class SourceFileResponse(SourceFileBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class SourceFileResponseList(BaseModel):
    files: list[SourceFileResponse] = field(default_factory=list)


class SourceFileDelete(BaseModel):
    id: int
    deleted: bool
