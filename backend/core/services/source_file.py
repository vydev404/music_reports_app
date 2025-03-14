# -*- coding: utf-8 -*-
from core.models.source_file import ProcessingStatus
from core.schemas import (
    SourceFileCreate,
    SourceFileDelete,
    SourceFileResponse,
    SourceFileResponseList,
    SourceFileUpdate,
)
from core.services.base import BaseService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class SourceFileService(BaseService):
    async def create(self, data: SourceFileCreate) -> SourceFileResponse:
        values = data.model_dump()
        try:
            result = await self.repository.create(values)
            return SourceFileResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_id(self, model_id: int) -> SourceFileResponse:
        try:
            result = await self.repository.get_by_id(model_id)
            if not result:
                raise HTTPException(status_code=404, detail="Item not found")
            return SourceFileResponse.model_validate(result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_many(self, limit: int, offset: int) -> SourceFileResponseList:
        try:
            result = SourceFileResponseList()
            db_result = await self.repository.get_many(limit, offset)
            result.files = [SourceFileResponse.model_validate(i) for i in db_result]
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_latest(self, last_n) -> SourceFileResponseList:
        result = SourceFileResponseList()
        try:
            db_result = await self.repository.get_latest(last_n)
            for source_file in db_result:
                result.files.append(SourceFileResponse.model_validate(source_file))
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_with_status(self, status: ProcessingStatus) -> SourceFileResponseList:
        result = SourceFileResponseList()
        try:
            db_result = await self.repository.get_by_status(status)
            result.files = [SourceFileResponse.model_validate(i) for i in db_result]
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_hash(self, model_hash: str) -> SourceFileResponse:
        pass

    async def update(self, model_id: int, data: SourceFileUpdate) -> SourceFileResponse:
        values = data.model_dump(exclude_unset=True)
        try:
            result = await self.repository.update(model_id, values)
            return SourceFileResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete(self, model_id: int) -> SourceFileDelete:
        try:
            result = await self.repository.delete(model_id)
            return SourceFileDelete(id=model_id, deleted=result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
