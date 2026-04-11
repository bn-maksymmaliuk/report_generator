from enum import Enum

class EmployeeField(str, Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    SALARY = "salary"
    AGE = "age"
    JOB = "job"