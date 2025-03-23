# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models import Base
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskProcessingStage(str, enum.Enum):
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    FILTERING = "FILTERING"
    REPORTING = "REPORTING"
    MOVING = "MOVING"


class TaskQueue(Base):
    __tablename__ = "tasks_queue"

    source_file_id: Mapped[int] = mapped_column(
        ForeignKey("source_files.id", ondelete="CASCADE")
    )
    source_file: Mapped["SourceFile"] = relationship(
        "SourceFile", back_populates="tasks"
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.PENDING,
    )
    error_stage: Mapped[TaskProcessingStage] = mapped_column(
        Enum(
            TaskProcessingStage,
            name="task_processing_stage",
        ),
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
