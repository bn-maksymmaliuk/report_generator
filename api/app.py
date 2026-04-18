from fastapi import FastAPI

from api.routes import router as reports_router
from application.jobs import JobRegistry
from application.use_cases.batch_runner import BatchRunner
from config.logger_setup import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title="Report Generator", version="1.0.0")

    registry = JobRegistry()
    app.state.registry = registry
    app.state.runner = BatchRunner(registry)

    app.include_router(reports_router)

    @app.get("/health", tags=["system"])
    async def health() -> dict:
        return {"status": "ok"}

    return app
