# -*- coding: utf-8 -*-
from fastapi import APIRouter
from core.config import settings
from . import music_routes, report_routes, source_file_routes

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["API_V1"],
)
router.include_router(music_routes.router)
router.include_router(report_routes.router)
router.include_router(source_file_routes.router)
