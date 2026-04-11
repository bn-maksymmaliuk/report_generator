import logging

from reports.base import BaseReport
from shared.types import Employee, EmployeeFieldName

logger = logging.getLogger(__name__)

class EmployeeReport(BaseReport):
    def __init__(self, min_salary: int = 3500, extra_fields: list[EmployeeFieldName] = []):
        self.min_salary = min_salary
        self.extra_fields = extra_fields

    async def process(self, data: list[Employee]) -> list[dict]:
        logger.info(f"Processing {len(data)} employees with min_salary={self.min_salary}")

        if len(self.extra_fields) > 0:
            logger.info(f"Found {len(self.extra_fields)} extra fields")

        result: list[dict] = []

        for row in data:
            salary = int(row["salary"])

            if salary > self.min_salary:
                base = {"name": row["name"], "job": row["job"]}
                extra = {field: row[field] for field in self.extra_fields}
                row_data = {**base, **extra}

                result.append(row_data)

        logger.info(f"Found {len(result)} employees matching criteria")

        return result