import json
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.app import create_app

CSV_CONTENT = (
    "ID,Name,Age,Job,Salary\n"
    "1,Ivan,38,Engineer,5000\n"
    "2,Petro,25,Admin,1500\n"
)


@pytest.fixture
def client():
    with TestClient(create_app()) as c:
        yield c


def _wait_job(client: TestClient, job_id: str, timeout: float = 5.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        response = client.get(f"/reports/jobs/{job_id}")
        assert response.status_code == 200
        body = response.json()
        if body["status"] in ("success", "failed"):
            return body
        time.sleep(0.05)
    raise AssertionError(f"Job {job_id} did not finish in time")


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_submit_batch_and_get_job(tmp_path, client):
    csv_file = tmp_path / "in.csv"
    csv_file.write_text(CSV_CONTENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    payload = {
        "jobs": [
            {
                "source_type": "csv",
                "source_path": str(csv_file),
                "output_type": "json",
                "output_dir": str(out_dir),
                "report_type": "employee",
                "params": {"min_salary": 3500},
            }
        ]
    }

    response = client.post("/reports/batch", json=payload)
    assert response.status_code == 202
    body = response.json()
    batch_id = body["batch_id"]
    job_id = body["job_ids"][0]

    job = _wait_job(client, job_id)
    assert job["status"] == "success"

    batch = client.get(f"/reports/batch/{batch_id}").json()
    assert batch["total"] == 1
    assert batch["jobs"][0]["id"] == job_id

    written = json.loads(Path(job["result_path"]).read_text(encoding="utf-8"))
    assert written == [{"Name": "Ivan", "Job": "Engineer"}]


def test_job_not_found(client):
    assert client.get("/reports/jobs/does-not-exist").status_code == 404


def test_invalid_payload_returns_422(client):
    response = client.post("/reports/batch", json={"jobs": []})
    assert response.status_code == 422
