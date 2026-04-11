from reports.base import BaseReport
from shared.types import Employee, EmployeeReportRow

class EmployeeReport(BaseReport):
    def __init__(self, min_salary: int = 3500):
        self.min_salary = min_salary

    async def process(self, data: list[Employee]) -> list[EmployeeReportRow]:
        result: list[EmployeeReportRow] = []

        for row in data:
            salary = int(row["salary"])

            if salary > self.min_salary:
                result.append(EmployeeReportRow(
                    name=row["name"],
                    job=row["job"],
                ))

        return result