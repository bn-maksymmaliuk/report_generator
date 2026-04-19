# Report Generator

Async REST service for batch generation of reports from tabular sources.
Currently supports one report type — `employee` (filtering by salary and a configurable set of fields).

## Requirements

- Python 3.11+
- dependencies from [requirements.txt](requirements.txt)

## Setup

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Running the server

```bash
python main.py
```

The server listens on `http://0.0.0.0:8000`. OpenAPI schema is available at `/docs`.

## Running tests

From the project root, with the venv activated:

```bash
pytest
pytest -v
pytest -k batch
```

Config is in [pytest.ini](pytest.ini). Async tests are enabled via `asyncio_mode = auto`.

## API

| Method | Path | Purpose |
|---|---|---|
| `GET`  | `/health` | Liveness check |
| `POST` | `/reports/batch` | Submit a batch of N jobs |
| `GET`  | `/reports/batch/{batch_id}` | Status of a batch and all its jobs |
| `GET`  | `/reports/jobs/{job_id}` | Status of a single job |
| `GET`  | `/reports/jobs/{job_id}/download` | Download the result file |

### Example request

```bash
curl -X POST http://localhost:8000/reports/batch \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [
      {
        "source_type": "csv",
        "source_path": "task_files/input_data.csv",
        "output_type": "json",
        "output_dir": "report_results",
        "report_type": "employee",
        "params": { "min_salary": 4000, "extra_fields": ["age"] }
      }
    ]
  }'
```

Response is `202 Accepted` with a `batch_id` and a list of `job_ids`. Jobs run in the background — status is polled separately.

### Request fields

- `source_type`: `csv`, `json` (`api`, `database` are declared in the schema but not implemented)
- `source_path`: path to the input file relative to the project root
- `output_type`: `csv`, `json`
- `output_dir`: output directory (created if missing)
- `report_type`: `employee`
- `params.min_salary`: `int >= 0`, default `3500` — rows with `salary <= min_salary` are filtered out
- `params.extra_fields`: extra columns to include, chosen from `id`/`name`/`age`/`job`/`salary` (base columns `name` and `job` are always present)

## Project layout

```
api/             FastAPI app and routes
application/     Use cases, factories, job registry
domain/          Abstractions (BaseSource, BaseOutput, BaseReport, types)
infrastructure/  Concrete sources, reports, and outputs
schemas/         Pydantic request schemas
config/          Logger configuration
tests/           Pytest suite
task_files/      Demo input data
```
