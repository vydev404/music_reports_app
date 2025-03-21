# -*- coding: utf-8 -*-
from sqlalchemy import select

from core.models import db_manager
from core.models.task_queue import TaskQueue, TaskStatus
from core.repositories.base import SQLAlchemyRepository


class TaskQueueRepository(SQLAlchemyRepository):
    model = TaskQueue

    async def get_by_status(self, status: TaskStatus):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.status == status)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_pending_tasks(self):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.status == TaskStatus.PENDING)
            result = await session.execute(query)
            return result.scalars().all()
