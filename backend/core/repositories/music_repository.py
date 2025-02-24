from sqlalchemy import select

from core.models import Music, db_manager
from .base import SQLAlchemyRepository


class MusicRepository(SQLAlchemyRepository):
    model = Music

    async def get_by_title(self, title: str):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.title == title)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_right_holder(self, right_holder: str):
        async with db_manager.session_getter() as session:
            query = select(self.model).where(self.model.right_holder == right_holder)
            result = await session.execute(query)
            return result.scalars().all()
