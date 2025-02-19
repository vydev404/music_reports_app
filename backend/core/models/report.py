import json
from tkinter import Text

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base


class Report(Base):
    __tablename__ = "reports"
    name: Mapped[str]
    file: Mapped[str]

    source_file_id: Mapped[int] = mapped_column(ForeignKey("processed_files.id", ondelete="CASCADE"))
    source_file: Mapped["ParsedFile"] = relationship("ParsedFile", back_populates="reports")
    used_music_ids: Mapped[str] = mapped_column(Text, nullable=True, default="[]")

    @property
    def music_ids(self) -> list[int]:
        return json.loads(self.used_music_ids)

    @music_ids.setter
    def music_ids(self, value: list[int]):
        self.used_music_ids = json.dumps(value)
