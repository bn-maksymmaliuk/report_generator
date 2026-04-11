from typing import TypedDict, Literal


class Employee(TypedDict):
    id: str
    name: str
    age: str
    job: str
    salary: str

EmployeeFieldName = Literal["id", "name", "age", "job", "salary"]
