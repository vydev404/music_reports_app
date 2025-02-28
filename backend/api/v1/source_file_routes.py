# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from api.dependencies import source_file_service
from core.schemas import APIResponse, SourceFileCreate, SourceFileResponse, SourceFileResponseList, SourceFileDelete, \
    SourceFileUpdate, format_response
from core.services.source_file import SourceFileService

router = APIRouter(prefix="/files", tags=["Source Files"])

@router.post("/", response_model=APIResponse[SourceFileResponse])
async def create(file_data: SourceFileCreate, request: Request, service: SourceFileService = Depends(source_file_service)):
    result =   await service.create(file_data)
    return format_response(request, result)
@router.get("/{file_id}", response_model=APIResponse[SourceFileResponse])
async def get_by_id(file_id: UUID, request: Request, service: SourceFileService = Depends(source_file_service)):
    result =  await service.get_by_id(file_id)
    return format_response(request, result)

@router.get("/", response_model=APIResponse[SourceFileResponseList])
async def get_files(
        request: Request,
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        last_n: int = Query(0, ge=0, le=50),
        service: SourceFileService = Depends(source_file_service)
):
    if last_n:
        result =  await service.get_latest(last_n=last_n)
    else:
        result = await service.get_many(limit, offset)
    return format_response(request, result)


@router.put("/{file_id}", response_model=APIResponse[SourceFileResponse])
async def update(
        request: Request,
        file_id: UUID,
        updates: SourceFileUpdate,
        service: SourceFileService = Depends(source_file_service)
):
    result =  await service.update(file_id, updates)
    return format_response(request, result)


@router.delete("/{file_id}", response_model=APIResponse[SourceFileDelete])
async def delete(
        request: Request,
        file_id: UUID,
        service: SourceFileService = Depends(source_file_service)
):
    result =  await service.delete(file_id)
    return format_response(request, result)

