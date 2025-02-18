from abc import ABC, abstractmethod


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
