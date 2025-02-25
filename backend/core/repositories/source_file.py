from sqlalchemy import select

from core.models import SourceFile, db_manager
from core.models.source_file import ProcessingStatus
from .base import SQLAlchemyRepository


class SourceFileRepository(SQLAlchemyRepository):
    model = SourceFile

    async def get_by_hash(self, file_hash: str):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.hash == file_hash)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_status(self, status: ProcessingStatus = ProcessingStatus.NEW):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.status == status)
            result = await session.execute(query)
            return result.scalars().all()
