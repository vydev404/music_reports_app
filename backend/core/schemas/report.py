from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class ReportBase(BaseModel):
    report_name: str
    report_file: Path
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
