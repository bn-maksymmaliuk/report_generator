import logging

from domain.reports.base import BaseReport
from domain.types import Employee, EmployeeFieldName

logger = logging.getLogger(__name__)

BASE_FIELDS: tuple[tuple[EmployeeFieldName, str], ...] = (
    ("name", "Name"),
    ("job", "Job"),
)


class EmployeeReport(BaseReport):
    def __init__(
        self,
        min_salary: int = 3500,
        extra_fields: list[EmployeeFieldName] | None = None,
    ):
        self.min_salary = min_salary
        self.extra_fields: list[EmployeeFieldName] = list(extra_fields or [])

    async def process(self, data: list[Employee]) -> list[dict]:
        logger.info(
            f"Processing {len(data)} employees with min_salary={self.min_salary}"
        )

        result: list[dict] = []
        skipped = 0

        for row in data:
            try:
                salary = int(row["salary"])
            except (KeyError, TypeError, ValueError):
                skipped += 1
                continue

            if salary <= self.min_salary:
                continue

            item: dict = {label: row[field] for field, label in BASE_FIELDS}
            for field in self.extra_fields:
                item[field] = row[field]

            result.append(item)

        if skipped:
            logger.warning(f"Skipped {skipped} rows with invalid salary")

        logger.info(f"Found {len(result)} employees matching criteria")
        return result
