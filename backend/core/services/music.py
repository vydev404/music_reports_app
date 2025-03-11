# -*- coding: utf-8 -*-
from core.schemas import (
    MusicCreate,
    MusicDelete,
    MusicResponse,
    MusicResponseList,
    MusicUpdate,
)
from core.services.base import BaseService
from fastapi import HTTPException
from proccessing.audio_tools import AudioMetadata
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class MusicService(BaseService):
    async def create(self, data: MusicCreate) -> MusicResponse:
        try:
            music_metadata = AudioMetadata().get_music_data(data.path).to_dict()
            values = music_metadata
            result = await self.repository.create(values)
            return MusicResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_id(self, model_id: int) -> MusicResponse:
        try:
            result = await self.repository.get_by_id(model_id)
            if not result:
                raise HTTPException(status_code=404, detail="Item not found")
            return MusicResponse.model_validate(result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_many(self, limit: int, offset: int) -> MusicResponseList:
        try:
            result = MusicResponseList()
            db_result = await self.repository.get_many(limit, offset)
            result.files = [MusicResponse.model_validate(i) for i in db_result]
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_latest(self, last_n) -> MusicResponseList:
        result = MusicResponseList()
        try:
            db_result = await self.repository.get_latest(last_n)
            for source_file in db_result:
                result.files.append(MusicResponse.model_validate(source_file))
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, model_id: int, data: MusicUpdate) -> MusicResponse:
        values = data.model_dump(exclude_unset=True)
        try:
            result = await self.repository.update(model_id, values)
            return MusicResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete(self, model_id: int) -> MusicDelete:
        try:
            result = await self.repository.delete(model_id)
            return MusicDelete(id=model_id, deleted=result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
