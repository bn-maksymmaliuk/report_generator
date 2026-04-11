from abc import ABC, abstractmethod
import logging

from shared.types import Employee

logger = logging.getLogger(__name__)

class BaseSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[Employee]:
        """Fetch and return normalized data."""
        ...

    @staticmethod
    def normalize_row(row: dict) -> Employee:
        normalized = {k.strip().lower(): v.strip() for k, v in row.items()}

        try:
            return Employee(
                id=normalized["id"],
                name=normalized["name"],
                age=normalized["age"],
                job=normalized["job"],
                salary=normalized["salary"],
            )
        except KeyError as e:
            logger.error(f"Missing field: {e.args[0]}")
            raise ValueError(f"Missing field: {e.args[0]}")
