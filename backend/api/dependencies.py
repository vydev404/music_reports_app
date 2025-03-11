# -*- coding: utf-8 -*-
from core.repositories import SourceFileRepository, MusicRepository, ReportRepository
from core.services.music import MusicService
from core.services.report import ReportService
from core.services.source_file import SourceFileService


def report_service():
    return ReportService(ReportRepository())


def music_service():
    return MusicService(MusicRepository())


def source_file_service():
    return SourceFileService(SourceFileRepository())
