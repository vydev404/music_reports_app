import json

from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base


class Report(Base):
    __tablename__ = "reports"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file: Mapped[str] = mapped_column(String(255), nullable=False)

    source_file_id: Mapped[int] = mapped_column(
        ForeignKey("source_files.id", ondelete="CASCADE")
    )
    source_file: Mapped["SourceFile"] = relationship(
        "SourceFile", back_populates="reports"
    )

    used_music: Mapped[list[dict]] = mapped_column(
        JSONB, nullable=True, server_default="[]"
    )
    # format [
    #     {
    #         "id": 1,
    #         "count": 2,
    #         "duration": "00:02:15",
    #         "title": "Song A"
    #     },
    #     {
    #         "id": 3,
    #         "count": 1,
    #         "duration": "00:01:30",
    #         "title": "Song B"
    #     }
    # ]
