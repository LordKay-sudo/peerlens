from fastapi import APIRouter

from peerlens import __version__
from peerlens.config import get_settings
from peerlens.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version=__version__,
        rag_demo_mode=not settings.rag_uses_llm(),
    )
