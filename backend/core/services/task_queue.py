# -*- coding: utf-8 -*-
from core.schemas import (
    TaskQueueCreate,
    TaskQueueDelete,
    TaskQueueResponse,
    TaskQueueResponseList,
    TaskQueueUpdate,
)
from core.services.base import BaseService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class TaskQueueService(BaseService):
    async def create(self, data: TaskQueueCreate) -> TaskQueueResponse:
        try:
            values = data.model_dump()
            result = await self.repository.create(values)
            return TaskQueueResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_id(self, model_id: int) -> TaskQueueResponse:
        try:
            result = await self.repository.get_by_id(model_id)
            if not result:
                raise HTTPException(status_code=404, detail="Item not found")
            return TaskQueueResponse.model_validate(result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_many(self, limit: int, offset: int) -> TaskQueueResponseList:
        try:
            result = TaskQueueResponseList()
            db_result = await self.repository.get_many(limit, offset)
            result.tasks = [TaskQueueResponse.model_validate(i) for i in db_result]
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_latest(self, last_n) -> TaskQueueResponseList:
        result = TaskQueueResponseList()
        try:
            db_result = await self.repository.get_latest(last_n)
            for source_file in db_result:
                result.tasks.append(TaskQueueResponse.model_validate(source_file))
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_pending(self) -> TaskQueueResponseList:
        try:
            result = TaskQueueResponseList()
            db_result = await self.repository.get_pending_tasks()
            result.tasks = [TaskQueueResponse.model_validate(i) for i in db_result]
            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, model_id: int, data: TaskQueueUpdate) -> TaskQueueResponse:
        values = data.model_dump(exclude_unset=True)
        try:
            result = await self.repository.update(model_id, values)
            return TaskQueueResponse.model_validate(result)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete(self, model_id: int) -> TaskQueueDelete:
        try:
            result = await self.repository.delete(model_id)
            return TaskQueueDelete(id=model_id, deleted=result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    pass
