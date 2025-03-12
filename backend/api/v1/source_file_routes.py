# -*- coding: utf-8 -*-
from api.dependencies import source_file_service
from api.v1.base_crud_router import BaseCRUDRouter
from core.schemas import (SourceFileCreate, SourceFileDelete,
                          SourceFileResponse, SourceFileResponseList,
                          SourceFileUpdate)

router = BaseCRUDRouter[
    SourceFileCreate,
    SourceFileUpdate,
    SourceFileResponse,
    SourceFileResponseList,
    SourceFileDelete,
](prefix="/files", tags=["Source Files"], service=source_file_service()).router

# @router.post("/", response_model=APIResponse[SourceFileResponse])
# async def create(file_data: SourceFileCreate, request: Request, service: SourceFileService = Depends(source_file_service)):
#     result =   await service.create(file_data)
#     return format_response(request, result)
# @router.get("/{file_id}", response_model=APIResponse[SourceFileResponse])
# async def get_by_id(file_id: int, request: Request, service: SourceFileService = Depends(source_file_service)):
#     result =  await service.get_by_id(file_id)
#     return format_response(request, result)
#
# @router.get("/", response_model=APIResponse[SourceFileResponseList])
# async def get_files(
#         request: Request,
#         limit: int = Query(100, ge=1, le=1000),
#         offset: int = Query(0, ge=0),
#         last_n: int = Query(0, le=50),
#         status: ProcessingStatus  = Query(ProcessingStatus.NEW),
#         service: SourceFileService = Depends(source_file_service)
# ):
#     if last_n:
#         result =  await service.get_latest(last_n=last_n)
#     elif status:
#         result = await service.get_with_status(status)
#     else:
#         result = await service.get_many(limit, offset)
#     return format_response(request, result)
#
#
# @router.put("/{file_id}", response_model=APIResponse[SourceFileResponse])
# async def update(
#         request: Request,
#         file_id: int,
#         updates: SourceFileUpdate,
#         service: SourceFileService = Depends(source_file_service)
# ):
#     result =  await service.update(file_id, updates)
#     return format_response(request, result)
#
#
# @router.delete("/{file_id}", response_model=APIResponse[SourceFileDelete])
# async def delete(
#         request: Request,
#         file_id: int,
#         service: SourceFileService = Depends(source_file_service)
# ):
#     result =  await service.delete(file_id)
#     return format_response(request, result)
