# -*- coding: utf-8 -*-
from dataclasses import field
from datetime import datetime

from pydantic import BaseModel


class TaskQueueBase(BaseModel):
    source_file_id: int


class TaskQueueCreate(TaskQueueBase):
    pass


class TaskQueueUpdate(BaseModel):
    status: str
    error_stage: str | None = None
    error_message: str | None = None


class TaskQueueResponse(TaskQueueBase):
    id: int
    status: str
    error_stage: str | None = None
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class TaskQueueResponseList(BaseModel):
    tasks: list[TaskQueueResponse] = field(default_factory=list)


class TaskQueueDelete(BaseModel):
    id: int
    deleted: bool
