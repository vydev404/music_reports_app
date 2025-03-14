# -*- coding: utf-8 -*-
from api.dependencies import report_service
from api.v1.base_crud_router import BaseCRUDRouter
from core.schemas import (
    ReportCreate,
    ReportDelete,
    ReportResponse,
    ReportResponseList,
    ReportUpdate,
)

router = BaseCRUDRouter[
    ReportCreate, ReportUpdate, ReportResponse, ReportResponseList, ReportDelete
](prefix="/reports", tags=["Reports"], service_instance=report_service).router
