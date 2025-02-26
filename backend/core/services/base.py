from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from core.repositories.base import AbstractRepository


class BaseService:

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def exists(self, model_id: UUID) -> bool:
        try:
            return await self.repository.exists(model_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
