# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Depends, Query
from api.dependencies import task_queue_service
from core.schemas import (
    TaskQueueCreate,
    TaskQueueDelete,
    TaskQueueResponse,
    TaskQueueResponseList,
    TaskQueueUpdate,
    format_response,
    APIResponse,
)
from core.schemas.task_queue import TaskQueueResponse, TaskQueueCreate
from core.services.task_queue import TaskQueueService

router = APIRouter(prefix="/tasks", tags=["Task Queue"])


@router.post("/", response_model=APIResponse[TaskQueueCreate])
async def create(
    file_data: TaskQueueCreate,
    request: Request,
    service: TaskQueueService = Depends(task_queue_service),
):
    result = await service.create(file_data)
    return format_response(request, result)


@router.get("/{task_id}", response_model=APIResponse[TaskQueueResponse])
async def get_by_id(
    task_id: int,
    request: Request,
    service: TaskQueueService = Depends(task_queue_service),
):
    result = await service.get_by_id(task_id)
    return format_response(request, result)


@router.get("/", response_model=APIResponse[TaskQueueResponseList])
async def get_files(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    last_n: int = Query(0, le=50),
    service: TaskQueueService = Depends(task_queue_service),
):
    if last_n:
        result = await service.get_latest(last_n=last_n)
    else:
        result = await service.get_many(limit, offset)
    return format_response(request, result)


@router.get("/", response_model=APIResponse[TaskQueueResponseList])
async def get_pending(
    request: Request,
    service: TaskQueueService = Depends(task_queue_service),
):
    result = await service.
    return format_response(request, result)


@router.put("/{task_id}", response_model=APIResponse[TaskQueueResponse])
async def update(
    request: Request,
    task_id: int,
    updates: TaskQueueUpdate,
    service: TaskQueueService = Depends(task_queue_service),
):
    result = await service.update(task_id, updates)
    return format_response(request, result)


@router.delete("/{task_id}", response_model=APIResponse[TaskQueueDelete])
async def delete(
    request: Request,
    task_id: int,
    service: TaskQueueService = Depends(task_queue_service),
):
    result = await service.delete(task_id)
    return format_response(request, result)
