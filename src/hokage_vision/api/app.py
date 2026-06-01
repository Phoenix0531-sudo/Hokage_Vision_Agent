from __future__ import annotations

from fastapi import FastAPI

from hokage_vision import __version__
from hokage_vision.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hokage Vision Agent API",
        version=__version__,
        description="Local API for mock-backed detection, agent workflows, dataset checks, and model comparison.",
    )
    app.include_router(router)
    return app


app = create_app()
