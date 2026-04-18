import asyncio
import logging
import uuid

from application.factories import build_pipeline
from application.jobs import Job, JobRegistry
from schemas.schemas import ReportJobRequest

logger = logging.getLogger(__name__)


class BatchRunner:
    def __init__(self, registry: JobRegistry, max_concurrency: int = 8):
        self.registry = registry
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._tasks: set[asyncio.Task] = set()

    async def submit(self, requests: list[ReportJobRequest]) -> tuple[str, list[Job]]:
        batch_id = uuid.uuid4().hex
        jobs: list[Job] = []

        for request in requests:
            job = await self.registry.create(batch_id)
            jobs.append(job)
            task = asyncio.create_task(self._run_job(job, request))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        logger.info(f"Submitted batch {batch_id} with {len(jobs)} job(s)")
        return batch_id, jobs

    async def wait_all(self) -> None:
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    async def _run_job(self, job: Job, request: ReportJobRequest) -> None:
        async with self._semaphore:
            await self.registry.mark_running(job.id)
            try:
                runner = build_pipeline(request)
                path = await runner.run(job_id=job.id)
                await self.registry.mark_success(job.id, path)
            except Exception as exc:
                logger.exception(f"Job {job.id} failed")
                await self.registry.mark_failed(
                    job.id, f"{type(exc).__name__}: {exc}"
                )
