import logging
from abc import ABC, abstractmethod

from domain.types import Employee

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ("id", "name", "age", "job", "salary")


class BaseSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[Employee]:
        """Fetch and return normalized data."""
        ...

    @staticmethod
    def normalize_row(row: dict) -> Employee:
        normalized = {
            k.strip().lower(): (v.strip() if isinstance(v, str) else v)
            for k, v in row.items()
            if k is not None
        }

        missing = [f for f in REQUIRED_FIELDS if not normalized.get(f)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        return Employee(
            id=normalized["id"],
            name=normalized["name"],
            age=normalized["age"],
            job=normalized["job"],
            salary=normalized["salary"],
        )
