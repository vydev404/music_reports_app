from sqlalchemy import String, JSON, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class SourceFile(Base):
    __tablename__ = "source_files"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    reports: Mapped["Report"] = relationship("Report", back_populates="source_file")
    tasks: Mapped[list["TaskQueue"]] = relationship(
        "TaskQueue", back_populates="source_file"
    )
