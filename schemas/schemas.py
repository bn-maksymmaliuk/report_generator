from enum import Enum

from pydantic import BaseModel, Field

from domain.types import EmployeeFieldName


class SourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"
    DATABASE = "database"


class OutputType(str, Enum):
    CSV = "csv"
    JSON = "json"


class ReportType(str, Enum):
    EMPLOYEE = "employee"


class EmployeeReportParams(BaseModel):
    min_salary: int = Field(default=3500, ge=0)
    extra_fields: list[EmployeeFieldName] = Field(default_factory=list)


class ReportJobRequest(BaseModel):
    source_type: SourceType
    source_path: str = Field(min_length=1)
    output_type: OutputType
    output_dir: str = Field(min_length=1)
    report_type: ReportType
    params: EmployeeReportParams = Field(default_factory=EmployeeReportParams)


class BatchReportRequest(BaseModel):
    jobs: list[ReportJobRequest] = Field(min_length=1)
