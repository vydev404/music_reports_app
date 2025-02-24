import uuid

from sqlalchemy import select

from core.models import Report, db_manager
from core.repositories.base import SQLAlchemyRepository


class ReportRepository(SQLAlchemyRepository):
    model = Report

    async def get_by_source_file_id(self, source_file_id: uuid.UUID):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.source_file_id == source_file_id)
            result = await session.execute(query)
            return result.scalars().all()
