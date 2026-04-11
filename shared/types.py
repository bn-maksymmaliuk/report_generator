from typing import TypedDict


class Employee(TypedDict):
    id: str
    name: str
    age: str
    job: str
    salary: str

class EmployeeReportRow(TypedDict):
    name: str
    job: str