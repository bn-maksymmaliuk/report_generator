from abc import ABC, abstractmethod

from shared.types import Employee

class BaseSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[Employee]:
        """Fetch and return normalized data."""
        ...

    @staticmethod
    def normalize_row(row: dict) -> dict:
        return {key.strip().lower(): val for key, val in row.items()}