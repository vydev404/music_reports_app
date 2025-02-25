# -*- coding: utf-8 -*-
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from api.dependencies import report_service
from core.schemas import APIResponse, ReportCreate, ReportResponse
from core.services.report import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=APIResponse[ReportResponse])
async def create(report_data: ReportCreate, service: ReportService = Depends(report_service)):
    return await service.create(report_data)

@router.get("/{report_id}", response_model=APIResponse[ReportResponse])
async def get_by_id(report_id: UUID, service: ReportService = Depends(report_service)):
    return await service.get_by_id(report_id)

@router.delete("/{report_id}", response_model=APIResponse[bool])
async def delete(report_id: UUID, service: ReportService = Depends(report_service)):
    return await service.delete(report_id)

@router.get("/", response_model=APIResponse[list[ReportResponse]])
async def get_many(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ReportService = Depends(report_service)
):
    return await service.get_many(limit, offset)
