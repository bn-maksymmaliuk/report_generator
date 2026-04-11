import logging
import time

from outputs.base import BaseOutput
from reports.base import BaseReport
from sources.base import BaseSource

logger = logging.getLogger(__name__)

class ReportRunner:
    def __init__(self, output: BaseOutput, source: BaseSource, report: BaseReport):
        self.output = output
        self.source = source
        self.report = report

    async def run(self) -> str:
        start = time.monotonic()

        logger.info(f"Starting report generation.")

        data = await self.source.fetch()

        filtered = await self.report.process(data)

        result = await self.output.write(filtered)

        elapsed = time.monotonic() - start
        logger.info(f"Report generated in {elapsed:.3f}s")

        return result
