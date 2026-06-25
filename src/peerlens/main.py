from contextlib import asynccontextmanager

from fastapi import FastAPI

from peerlens import __version__
from peerlens.api.router import api_router
from peerlens.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_settings()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "Open infrastructure for transparent research quality signals. "
            "PeerLens fetches paper metadata and runs explainable automated checks — "
            "decision support, not a proprietary credit rating."
        ),
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
