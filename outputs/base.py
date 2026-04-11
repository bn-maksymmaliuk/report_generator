from abc import ABC, abstractmethod

class BaseOutput(ABC):
    @abstractmethod
    async def write(self, data: list[dict]) -> str:
        ...