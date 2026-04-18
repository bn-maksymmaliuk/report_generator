from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse

from application.jobs import JobRegistry
from application.use_cases.batch_runner import BatchRunner
from schemas.schemas import BatchReportRequest

router = APIRouter(prefix="/reports", tags=["reports"])


def get_registry(request: Request) -> JobRegistry:
    return request.app.state.registry


def get_runner(request: Request) -> BatchRunner:
    return request.app.state.runner


@router.post("/batch", status_code=status.HTTP_202_ACCEPTED)
async def submit_batch(
    payload: BatchReportRequest,
    runner: BatchRunner = Depends(get_runner),
) -> dict:
    batch_id, jobs = await runner.submit(payload.jobs)
    return {"batch_id": batch_id, "job_ids": [job.id for job in jobs]}


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: str,
    registry: JobRegistry = Depends(get_registry),
) -> dict:
    job = await registry.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()


@router.get("/batch/{batch_id}")
async def get_batch(
    batch_id: str,
    registry: JobRegistry = Depends(get_registry),
) -> dict:
    jobs = await registry.by_batch(batch_id)
    if not jobs:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {
        "batch_id": batch_id,
        "total": len(jobs),
        "jobs": [job.to_dict() for job in jobs],
    }


@router.get("/jobs/{job_id}/download")
async def download_job_result(
    job_id: str,
    registry: JobRegistry = Depends(get_registry),
) -> FileResponse:
    job = await registry.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.result_path:
        raise HTTPException(status_code=409, detail=f"Job is {job.status.value}")
    return FileResponse(job.result_path, filename=job.result_path.rsplit("/", 1)[-1])
