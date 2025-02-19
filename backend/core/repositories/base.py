from abc import ABC, abstractmethod

from sqlalchemy import select

from core.models import db_manager


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, values: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, model_id: int):
        raise NotImplementedError

    @abstractmethod
    async def exists(self, model_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, model_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, limit: int, offset: int = 0):
        raise NotImplementedError

    @abstractmethod
    async def get_latest(self, last_n: int):
        raise NotImplementedError

    @abstractmethod
    async def update(self, model_id: int, values: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create(self, values: dict):
        async with db_manager.session_getter() as session:
            record = self.model(**values)
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record

    async def get_by_id(self, model_id: int):
        async with db_manager.session_getter() as session:
            return await session.get(self.model, model_id)

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

