# -*- coding: utf-8 -*-
from core.config import settings
from fastapi import APIRouter

from . import music_routes, report_routes, source_file_routes, task_queue_routes

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(music_routes.router)
router.include_router(report_routes.router)
router.include_router(source_file_routes.router)

router.include_router(task_queue_routes.router)
