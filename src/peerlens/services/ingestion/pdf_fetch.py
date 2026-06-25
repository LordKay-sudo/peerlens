import httpx

from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import IngestionError


async def fetch_arxiv_pdf(arxiv_id: str, settings: Settings | None = None) -> bytes:
    settings = settings or get_settings()
    base_id = arxiv_id.split("v")[0]
    url = f"https://arxiv.org/pdf/{base_id}.pdf"

    async with httpx.AsyncClient(
        timeout=settings.request_timeout_seconds,
        follow_redirects=True,
    ) as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise IngestionError(f"Could not download arXiv PDF ({response.status_code})")

        content_type = response.headers.get("content-type", "")
        if "pdf" not in content_type and not response.content.startswith(b"%PDF"):
            raise IngestionError("arXiv did not return a PDF for this identifier")

        return response.content
