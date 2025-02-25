import uuid
from datetime import datetime

from pydantic import BaseModel


class MusicBase(BaseModel):
    name: str
    path: str
    created_at: datetime
    updated_at: datetime | None


class MusicCreate(MusicBase):
    pass


class MusicUpdate(BaseModel):
    updated_at: datetime
    is_alive: bool


class MusicResponse(BaseModel):
    id: uuid.UUID
    name: str
    title: str
    artist: str
    album: str
    right_holder: str

    class Config:
        from_attributes = True
