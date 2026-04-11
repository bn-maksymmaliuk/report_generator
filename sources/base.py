from abc import ABC, abstractmethod

from shared.types import Employee

class BaseSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[Employee]:
        """Fetch and return normalized data."""
        ...

    @staticmethod
    def normalize_row(row: dict) -> Employee:
        normalized = {key.strip().lower(): val for key, val in row.items()}

        return Employee(
            id=normalized.get("id", '').strip(),
            name=normalized.get("name", '').strip(),
            age=normalized.get("age", '').strip(),
            job=normalized.get("job", '').strip(),
            salary=normalized.get("salary", '').strip(),
        )