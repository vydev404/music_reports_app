from fastapi import APIRouter
from api.v1 import music_routes, report_routes, source_file_routes

router = APIRouter()

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(music_routes.router)
api_v1_router.include_router(report_routes.router)
api_v1_router.include_router(source_file_routes.router)

router.include_router(api_v1_router)