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
    id: int
    status: str
    error_stage: str | None = None
    error_message: str | None = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class SourceFileDelete(BaseModel):
    id: int
    deleted: bool
