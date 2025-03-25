# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query, Request

from api.dependencies import music_service
from core.schemas import (
    APIResponse,
    MusicCreate,
    MusicDelete,
    MusicResponse,
    MusicUpdate,
    format_response,
    MusicResponseList,
)
from core.services.music import MusicService

router = APIRouter(prefix="/musics", tags=["Music"])


@router.post("/", response_model=APIResponse[MusicResponse])
async def create(
    music_data: MusicCreate,
    request: Request,
    service: MusicService = Depends(music_service),
):
    result = await service.create(music_data)
    return format_response(request, result)


@router.get("/search", response_model=APIResponse[MusicResponse])
async def search(
    request: Request,
    music_name: str = Query(default=None),
    service: MusicService = Depends(music_service),
):
    result = await service.get_by_name(music_name)
    return format_response(request, result)


@router.get("/{music_id}", response_model=APIResponse[MusicResponse])
async def get_by_id(
    request: Request, music_id: int, service: MusicService = Depends(music_service)
):
    result = await service.get_by_id(music_id)
    return format_response(request, result)


@router.get("/", response_model=APIResponse[MusicResponseList])
async def get_files(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    last_n: int = Query(0, le=50),
    service: MusicService = Depends(music_service),
):
    if last_n:
        result = await service.get_latest(last_n=last_n)
    else:
        result = await service.get_many(limit, offset)
    return format_response(request, result)


@router.put("/{music_id}", response_model=APIResponse[MusicResponse])
async def update(
    request: Request,
    music_id: int,
    updates: MusicUpdate,
    service: MusicService = Depends(music_service),
):
    result = await service.update(music_id, updates)
    return format_response(request, result)


@router.delete("/{music_id}", response_model=APIResponse[MusicDelete])
async def delete(
    request: Request, music_id: int, service: MusicService = Depends(music_service)
):
    result = await service.delete(music_id)
    return format_response(request, result)
