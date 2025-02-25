from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.repositories.base import AbstractRepository


class BaseService:

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def create(self, data: BaseModel) -> BaseModel:
        values = data.model_dump()
        try:
            result = await self.repository.create(values)
            return result
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete(self, model_id: UUID) -> bool:
        try:
            return await self.repository.delete(model_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def exists(self, model_id: UUID) -> bool:
        try:
            return await self.repository.exists(model_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_id(self, model_id: UUID):
        try:
            result = await self.repository.get_by_id(model_id)
            if not result:
                raise HTTPException(status_code=404, detail="Item not found")
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_many(self, limit: int = 100, offset: int = 0):
        try:
            return await self.repository.get_many(limit, offset)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_latest(self, last_n: int):
        try:
            return await self.repository.get_latest(last_n)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, model_id: UUID, values: dict):
        try:
            return await self.repository.update(model_id, values)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
