from abc import ABC, abstractmethod

from shared.types import Employee

class BaseReport(ABC):
    @abstractmethod
    async def process(self, data: list[Employee]) -> list[dict]: ...