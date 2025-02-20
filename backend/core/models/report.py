import json

from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base


class Report(Base):
    __tablename__ = "reports"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file: Mapped[str] = mapped_column(String(255), nullable=False)

    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_files.id", ondelete="CASCADE"))
    source_file: Mapped["SourceFile"] = relationship("SourceFile", back_populates="reports")
    used_music_ids: Mapped[str] = mapped_column(Text, nullable=True, server_default="[]")

    @property
    def music_ids(self) -> list[int]:
        return json.loads(self.used_music_ids)

    @music_ids.setter
    def music_ids(self, value: list[int]):
        self.used_music_ids = json.dumps(value)
