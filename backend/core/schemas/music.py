import uuid
from dataclasses import field
from datetime import datetime

from pydantic import BaseModel


class MusicBase(BaseModel):
    name: str
    path: str


class MusicCreate(MusicBase):
    pass


class MusicUpdate(BaseModel):
    name: str | None = None
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    right_holder: str | None = None
    is_alive: bool | None = None


class MusicResponse(BaseModel):
    id: int
    name: str
    title: str
    artist: str
    album: str
    right_holder: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class MusicResponseList(BaseModel):
    files: list[MusicResponse] = field(default_factory=list)


class MusicDelete(BaseModel):
    id: int
    deleted: bool
