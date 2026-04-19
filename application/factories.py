from application.use_cases.generate_report import ReportRunner
from domain.outputs.base import BaseOutput
from domain.reports.base import BaseReport
from domain.sources.base import BaseSource
from infrastructure.outputs.csv_output import CsvOutput
from infrastructure.outputs.json_output import JsonOutput
from infrastructure.reports.employee_report import EmployeeReport
from infrastructure.sources.csv_source import CsvSource
from infrastructure.sources.json_source import JsonSource
from schemas.schemas import (
    OutputType,
    ReportJobRequest,
    ReportType,
    SourceType,
)


def build_source(request: ReportJobRequest) -> BaseSource:
    if request.source_type is SourceType.CSV:
        return CsvSource(request.source_path)
    if request.source_type is SourceType.JSON:
        return JsonSource(request.source_path)
    raise ValueError(f"Unsupported source type: {request.source_type.value}")


def build_output(request: ReportJobRequest) -> BaseOutput:
    if request.output_type is OutputType.JSON:
        return JsonOutput(request.output_dir, file_prefix=request.report_type.value)
    if request.output_type is OutputType.CSV:
        return CsvOutput(request.output_dir, file_prefix=request.report_type.value)
    raise ValueError(f"Unsupported output type: {request.output_type.value}")


def build_report(request: ReportJobRequest) -> BaseReport:
    if request.report_type is ReportType.EMPLOYEE:
        return EmployeeReport(
            min_salary=request.params.min_salary,
            extra_fields=request.params.extra_fields,
        )

def build_pipeline(request: ReportJobRequest) -> ReportRunner:
    return ReportRunner(
        source=build_source(request),
        report=build_report(request),
        output=build_output(request),
    )
