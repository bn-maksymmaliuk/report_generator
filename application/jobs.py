from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Job:
    id: str
    batch_id: str
    status: JobStatus = JobStatus.PENDING
    result_path: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @property
    def duration(self) -> float | None:
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "status": self.status.value,
            "result_path": self.result_path,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration": self.duration,
        }


class JobRegistry:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = asyncio.Lock()

    async def create(self, batch_id: str) -> Job:
        job = Job(id=uuid.uuid4().hex, batch_id=batch_id)
        async with self._lock:
            self._jobs[job.id] = job
        return job

    async def get(self, job_id: str) -> Job | None:
        async with self._lock:
            return self._jobs.get(job_id)

    async def by_batch(self, batch_id: str) -> list[Job]:
        async with self._lock:
            return [job for job in self._jobs.values() if job.batch_id == batch_id]

    async def mark_running(self, job_id: str) -> None:
        async with self._lock:
            job = self._jobs[job_id]
            job.status = JobStatus.RUNNING
            job.started_at = datetime.now(timezone.utc)

    async def mark_success(self, job_id: str, result_path: str) -> None:
        async with self._lock:
            job = self._jobs[job_id]
            job.status = JobStatus.SUCCESS
            job.result_path = result_path
            job.finished_at = datetime.now(timezone.utc)

    async def mark_failed(self, job_id: str, error: str) -> None:
        async with self._lock:
            job = self._jobs[job_id]
            job.status = JobStatus.FAILED
            job.error = error
            job.finished_at = datetime.now(timezone.utc)
