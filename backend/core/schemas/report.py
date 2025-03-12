from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class ReportBase(BaseModel):
    report_name: str
    report_file: str
    source_file: int


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    modified_at: datetime
    report_name: str | None = None
    report_file: Path | None = None


class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class ReportResponseList(BaseModel):
    reports: list[ReportResponse] = Field(default=list)


class ReportDelete(BaseModel):
    id: int
    deleted: bool
