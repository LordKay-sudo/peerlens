from datetime import datetime

import httpx

from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import IngestionError
from peerlens.models.schemas import PaperMetadata, PaperSource
from peerlens.services.ingestion.identifiers import ParsedIdentifier


def _parse_arxiv_date(published: str | None) -> datetime | None:
    if not published:
        return None
    try:
        return datetime.fromisoformat(published.replace("Z", "+00:00"))
    except ValueError:
        return None


async def fetch_from_arxiv(
    parsed: ParsedIdentifier,
    settings: Settings | None = None,
) -> PaperMetadata:
    settings = settings or get_settings()
    arxiv_id = parsed.value.split("v")[0]
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise IngestionError(f"arXiv API returned {response.status_code}")

        text = response.text
        if "<entry>" not in text:
            raise IngestionError(f"No arXiv paper found for {parsed.raw}")

    title = _extract_tag(text, "title")
    abstract = _extract_tag(text, "summary")
    published = _extract_tag(text, "published")
    authors = _extract_all(text, "name")
    categories = _extract_all(text, "category", attr="term")

    return PaperMetadata(
        identifier=parsed.raw,
        source=PaperSource.ARXIV,
        title=_clean_text(title),
        authors=[_clean_text(a) for a in authors],
        abstract=_clean_text(abstract) or None,
        published=_parse_arxiv_date(published),
        url=f"https://arxiv.org/abs/{arxiv_id}",
        keywords=categories,
    )


def _extract_tag(xml: str, tag: str, attr: str | None = None) -> str:
    if attr:
        pattern = rf'<{tag}[^>]*{attr}="([^"]+)"'
    else:
        pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    match = __import__("re").search(pattern, xml, __import__("re").DOTALL)
    return match.group(1).strip() if match else ""


def _extract_all(xml: str, tag: str, attr: str | None = None) -> list[str]:
    import re

    if attr:
        pattern = rf'<{tag}[^>]*{attr}="([^"]+)"'
        return re.findall(pattern, xml)
    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    return [m.strip() for m in re.findall(pattern, xml, re.DOTALL)]


def _clean_text(value: str) -> str:
    import re

    return re.sub(r"\s+", " ", value).strip()
