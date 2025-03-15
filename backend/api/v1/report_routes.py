# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query, Request
from api.dependencies import report_service
from core.schemas import (
    APIResponse,
    ReportCreate,
    ReportResponse,
    format_response,
    ReportResponseList,
    ReportUpdate,
    ReportDelete,
)
from core.services.report import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/", response_model=APIResponse[ReportResponse])
async def create(
    file_data: ReportCreate,
    request: Request,
    service: ReportService = Depends(report_service),
):
    result = await service.create(file_data)
    return format_response(request, result)


@router.get("/{report_id}", response_model=APIResponse[ReportResponse])
async def get_by_id(
    report_id: int,
    request: Request,
    service: ReportService = Depends(report_service),
):
    result = await service.get_by_id(report_id)
    return format_response(request, result)


@router.get("/", response_model=APIResponse[ReportResponseList])
async def get_files(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    last_n: int = Query(0, le=50),
    service: ReportService = Depends(report_service),
):
    if last_n:
        result = await service.get_latest(last_n=last_n)
    else:
        result = await service.get_many(limit, offset)
    return format_response(request, result)


@router.put("/{report_id}", response_model=APIResponse[ReportResponse])
async def update(
    request: Request,
    report_id: int,
    updates: ReportUpdate,
    service: ReportService = Depends(report_service),
):
    result = await service.update(report_id, updates)
    return format_response(request, result)


@router.delete("/{report_id}", response_model=APIResponse[ReportDelete])
async def delete(
    request: Request,
    report_id: int,
    service: ReportService = Depends(report_service),
):
    result = await service.delete(report_id)
    return format_response(request, result)
