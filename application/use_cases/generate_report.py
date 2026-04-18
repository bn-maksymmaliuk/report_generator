import logging
import time

from domain.outputs.base import BaseOutput
from domain.reports.base import BaseReport
from domain.sources.base import BaseSource

logger = logging.getLogger("RUNNER")


class _JobAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[job={self.extra['job_id']}] {msg}", kwargs


class ReportRunner:
    def __init__(self, output: BaseOutput, source: BaseSource, report: BaseReport):
        self.output = output
        self.source = source
        self.report = report

    async def run(self, job_id: str | None = None) -> str:
        log = _JobAdapter(logger, {"job_id": job_id or "-"})
        start = time.monotonic()

        log.info("Starting report generation")

        data = await self.source.fetch()
        log.info(f"Fetched {len(data)} rows from source")

        filtered = await self.report.process(data)
        log.info(f"Report produced {len(filtered)} rows")

        result = await self.output.write(filtered)

        elapsed = time.monotonic() - start
        log.info(f"Report generated in {elapsed:.3f}s -> {result}")

        return result
