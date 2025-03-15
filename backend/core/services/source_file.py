# -*- coding: utf-8 -*-
from pathlib import Path

from core.schemas import (
    SourceFileCreate,
    SourceFileDelete,
    SourceFileResponse,
    SourceFileResponseList,
    SourceFileUpdate,
    SourceFileBase,
)
from core.services.base import BaseService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.files_tools import FileUtils as file_utility


class SourceFileService(BaseService):
    async def create(self, data: SourceFileCreate) -> SourceFileResponse:
        try:
            file_path = Path(data.path)
            print(type(file_path), file_path)
            file_metadata_object = SourceFileBase.model_validate(
                file_utility.get_file_metadata(file_path).to_dict()
            )
            file_metadata_object.hash = file_utility.calculate_file_hash(file_path)
            file_in_db = await self.repository.get_by_hash(file_metadata_object.hash)
            if file_in_db:  # test option for excluding unique constrains error
                file_metadata_object.hash += "1"
            values = file_metadata_object.model_dump()
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
