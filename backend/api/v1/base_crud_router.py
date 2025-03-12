# -*- coding: utf-8 -*-
from typing import Generic, Type, TypeVar

from core.schemas.api_response import APIResponse, format_response
from core.services.base import BaseService
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel

TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)
TResponseList = TypeVar("TResponseList", bound=BaseModel)
TDelete = TypeVar("TDelete", bound=BaseModel)


class BaseCRUDRouter(Generic[TCreate, TUpdate, TResponse, TResponseList, TDelete]):
    def __init__(self, prefix: str, tags: list[str], service: Type[BaseService]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.service = service

        @self.router.post("/", response_model=APIResponse[TResponse])
        async def create(
            request: Request,
            data: TCreate,
            service: BaseService = Depends(self.service),
        ):
            result = await service.create(data)
            return format_response(request, result)

        @self.router.get("/{item_id}", response_model=APIResponse[TResponse])
        async def get_by_id(
            request: Request, item_id: int, service: BaseService = Depends(self.service)
        ):
            result = await service.get_by_id(item_id)
            return format_response(request, result)

        @self.router.get("/", response_model=APIResponse[TResponseList])
        async def get_many(
            request: Request,
            limit: int = Query(100, ge=1, le=1000),
            offset: int = Query(0, ge=0),
            last_n: int = Query(0, le=50),
            service: BaseService = Depends(self.service),
        ):
            if last_n:
                result = await service.get_latest(last_n=last_n)
            else:
                result = await service.get_many(limit, offset)
            return format_response(request, result)

        @self.router.put("/{item_id}", response_model=APIResponse[TResponse])
        async def update(
            request: Request,
            item_id: int,
            updates: TUpdate,
            service: BaseService = Depends(self.service),
        ):
            result = await service.update(item_id, updates)
            return format_response(request, result)

        @self.router.delete("/{item_id}", response_model=APIResponse[TDelete])
        async def delete(
            request: Request, item_id: int, service: BaseService = Depends(service)
        ):
            result = await service.delete(item_id)
            return format_response(request, result)
