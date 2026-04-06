from abc import ABC, abstractmethod


class BaseSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[dict]: ...