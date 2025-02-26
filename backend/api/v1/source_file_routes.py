# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from api.dependencies import source_file_service
from core.schemas import APIResponse, SourceFileCreate, SourceFileResponse, SourceFileResponseList, SourceFileDelete
from core.services.source_file import SourceFileService

router = APIRouter(prefix="/files", tags=["Source Files"])

@router.post("/", response_model=APIResponse[SourceFileResponse])
async def create(file_data: SourceFileCreate, service: SourceFileService = Depends(source_file_service)):
    return await service.create(file_data)

@router.get("/{file_id}", response_model=APIResponse[SourceFileResponse])
async def get_by_id(file_id: UUID, service: SourceFileService = Depends(source_file_service)):
    return await service.get_by_id(file_id)

@router.get("/", response_model=APIResponse[SourceFileResponseList])
async def get_many(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    last_n: int = Query(0, ge=1, le=50),
    service: SourceFileService = Depends(source_file_service)
):
    if last_n:
        return await service.get_latest(last_n=last_n)
    return await service.get_many(limit, offset)

@router.delete("/{file_id}", response_model=APIResponse[SourceFileDelete])
async def delete(file_id: UUID, service: SourceFileService = Depends(source_file_service)):
    return await service.delete(file_id)
