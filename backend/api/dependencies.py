# -*- coding: utf-8 -*-
from core.repositories import (
    SourceFileRepository,
    MusicRepository,
    ReportRepository,
    TaskQueueRepository,
)
from core.services.base import BaseService
from core.services.music import MusicService
from core.services.report import ReportService
from core.services.source_file import SourceFileService
from core.services.task_queue import TaskQueueService


def report_service() -> BaseService:
    return ReportService(ReportRepository())


def music_service() -> BaseService:
    return MusicService(MusicRepository())


def source_file_service() -> BaseService:
    return SourceFileService(SourceFileRepository())


def task_queue_service() -> BaseService:
    return TaskQueueService(TaskQueueRepository())
