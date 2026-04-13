from abc import ABC, abstractmethod

from domain.types import Employee

class BaseReport(ABC):
    @abstractmethod
    async def process(self, data: list[Employee]) -> list[dict]: ...