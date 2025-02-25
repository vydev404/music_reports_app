# -*- coding: utf-8 -*-
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from api.dependencies import music_service
from core.schemas import APIResponse, MusicCreate, MusicResponse
from core.services.music import MusicService

router = APIRouter(prefix="/music", tags=["Music"])

@router.post("/", response_model=APIResponse[MusicResponse])
async def create(music_data: MusicCreate, service: MusicService = Depends(music_service)):
    return await service.create(music_data)

@router.get("/{music_id}", response_model=APIResponse[MusicResponse])
async def get_by_id(music_id: UUID, service: MusicService = Depends(music_service)):
    return await service.get_by_id(music_id)

@router.delete("/{music_id}", response_model=APIResponse[bool])
async def delete(music_id: UUID, service: MusicService = Depends(music_service)):
    return await service.delete(music_id)

@router.get("/", response_model=APIResponse[list[MusicResponse]])
async def get_many(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: MusicService = Depends(music_service)
):
    return await service.get_many(limit, offset)
