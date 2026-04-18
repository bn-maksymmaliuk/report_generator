import asyncio
import json
from pathlib import Path

import pytest

from application.jobs import JobRegistry, JobStatus
from application.use_cases.batch_runner import BatchRunner
from schemas.schemas import (
    BatchReportRequest,
    EmployeeReportParams,
    OutputType,
    ReportJobRequest,
    ReportType,
    SourceType,
)

CSV_CONTENT = (
    "ID,Name,Age,Job,Salary\n"
    "1,Ivan,38,Engineer,5000\n"
    "2,Olena,30,Biologist,4000\n"
    "3,Petro,25,Admin,1500\n"
)


def make_request(source: Path, out_dir: Path, min_salary: int = 3500) -> ReportJobRequest:
    return ReportJobRequest(
        source_type=SourceType.CSV,
        source_path=str(source),
        output_type=OutputType.JSON,
        output_dir=str(out_dir),
        report_type=ReportType.EMPLOYEE,
        params=EmployeeReportParams(min_salary=min_salary),
    )


async def _wait_for_completion(registry: JobRegistry, job_id: str, timeout: float = 5.0):
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        job = await registry.get(job_id)
        if job and job.status in (JobStatus.SUCCESS, JobStatus.FAILED):
            return job
        await asyncio.sleep(0.02)
    raise AssertionError(f"Job {job_id} did not complete in {timeout}s")


async def test_concurrent_jobs_complete_and_write_output(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(CSV_CONTENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    registry = JobRegistry()
    runner = BatchRunner(registry, max_concurrency=4)

    requests = [make_request(csv_file, out_dir) for _ in range(3)]
    batch_id, jobs = await runner.submit(requests)
    await runner.wait_all()

    results = [await registry.get(job.id) for job in jobs]
    assert all(j.status == JobStatus.SUCCESS for j in results)
    assert all(j.batch_id == batch_id for j in results)

    for job in results:
        payload = json.loads(Path(job.result_path).read_text(encoding="utf-8"))
        assert payload == [
            {"Name": "Ivan", "Job": "Engineer"},
            {"Name": "Olena", "Job": "Biologist"},
        ]


async def test_partial_failure_does_not_break_siblings(tmp_path):
    good = tmp_path / "good.csv"
    good.write_text(CSV_CONTENT, encoding="utf-8")
    bad = tmp_path / "missing.csv"
    out_dir = tmp_path / "out"

    registry = JobRegistry()
    runner = BatchRunner(registry)

    _, jobs = await runner.submit(
        [make_request(good, out_dir), make_request(bad, out_dir)]
    )
    await runner.wait_all()

    good_job = await registry.get(jobs[0].id)
    bad_job = await registry.get(jobs[1].id)

    assert good_job.status == JobStatus.SUCCESS
    assert bad_job.status == JobStatus.FAILED
    assert "FileNotFoundError" in bad_job.error
