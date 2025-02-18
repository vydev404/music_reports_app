from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from core.models import db_manager


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, values: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, model_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update(self, model_id: int, values: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create(self, values: dict):
        async with db_manager.session_getter() as session:
            stmt = insert(self.model).values(**values).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def get_by_id(self, model_id: int):
        async with db_manager.session_getter() as session:
            result = await session.get(self.model, model_id)
            return result

    async def get_all(self):
        async with db_manager.session_getter() as session:
            query = select(self.model)
            result = await session.execute(query)
            result = [row[0].to_read_model() for row in result.all()]
            return result

    async def update(self, model_id: int, values: dict):
        async with db_manager.session_getter() as session:
            result = await session.get(self.model, model_id)
            result = result.update(values)
            await session.refresh(result)
            await session.commit()
            return result
