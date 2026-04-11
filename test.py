import asyncio
import logging
from app.sources.csv_source import CsvSource
from app.reports.employee_report import EmployeeReport
from app.outputs.json_output import JsonOutput
from app.core.runner import ReportRunner
from app.config.logger_setup import setup_logging

setup_logging()

logger = logging.getLogger("test")

async def main():
    logger.info("Application started")

    runner = ReportRunner(
        source=CsvSource("task_files/input_data.csv"),
        report=EmployeeReport(),
        output=JsonOutput("report_results")
    )

    result = await runner.run()
    print(result)


asyncio.run(main())