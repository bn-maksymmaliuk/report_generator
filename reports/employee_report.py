import logging

from reports.base import BaseReport
from shared.types import Employee, EmployeeReportRow

logger = logging.getLogger(__name__)

class EmployeeReport(BaseReport):
    def __init__(self, min_salary: int = 3500):
        self.min_salary = min_salary

    async def process(self, data: list[Employee]) -> list[EmployeeReportRow]:
        logger.info(f"Processing {len(data)} employees with min_salary={self.min_salary}")
        result: list[EmployeeReportRow] = []


        for row in data:
            salary = int(row["salary"])

            if salary > self.min_salary:
                result.append(EmployeeReportRow(
                    name=row["name"],
                    job=row["job"],
                ))

        logger.info(f"Found {len(result)} employees matching criteria")

        return result