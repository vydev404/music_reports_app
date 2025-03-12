from uuid import UUID

from core.repositories.base import AbstractRepository
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError


class BaseService:

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def create(self, data: BaseModel) -> BaseModel:
        pass

    async def get_by_id(self, model_id: int) -> BaseModel:
        pass

    async def get_many(self, limit: int, offset: int) -> BaseModel:
        pass

    async def get_latest(self, last_n: int) -> BaseModel:
        pass

    async def update(self, data: BaseModel) -> BaseModel:
        pass

    async def delete(self, model_id: int) -> BaseModel:
        pass

    async def exists(self, model_id: int) -> bool:
        try:
            return await self.repository.exists(model_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
