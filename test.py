import asyncio
import logging
from domain.sources import CsvSource
from domain.reports import EmployeeReport
from domain.outputs import JsonOutput
from application.use_cases import ReportRunner
from config.logger_setup import setup_logging

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