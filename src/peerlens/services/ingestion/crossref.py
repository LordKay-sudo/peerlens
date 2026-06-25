from datetime import datetime

import httpx

from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import IngestionError
from peerlens.models.schemas import PaperMetadata, PaperSource
from peerlens.services.ingestion.identifiers import ParsedIdentifier


def _parse_crossref_date(parts: list[int] | None) -> datetime | None:
    if not parts:
        return None
    year = parts[0]
    month = parts[1] if len(parts) > 1 else 1
    day = parts[2] if len(parts) > 2 else 1
    try:
        return datetime(year, month, day)
    except ValueError:
        return datetime(year, 1, 1)


async def fetch_from_crossref(
    parsed: ParsedIdentifier,
    settings: Settings | None = None,
) -> PaperMetadata:
    settings = settings or get_settings()
    url = f"https://api.crossref.org/works/{parsed.value}"
    headers = {"User-Agent": f"PeerLens/0.1 (mailto:{settings.crossref_mailto})"}

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            raise IngestionError(f"No Crossref record found for DOI {parsed.value}")
        if response.status_code != 200:
            raise IngestionError(f"Crossref API returned {response.status_code}")

        payload = response.json().get("message", {})

    title_parts = payload.get("title") or []
    title = title_parts[0] if title_parts else "Untitled"
    authors = [
        " ".join(filter(None, [a.get("given"), a.get("family")]))
        for a in payload.get("author", [])
    ]
    abstract = payload.get("abstract")
    if abstract:
        abstract = _strip_jats(abstract)

    date_parts = None
    for key in ("published-print", "published-online", "created"):
        if key in payload and "date-parts" in payload[key]:
            date_parts = payload[key]["date-parts"][0]
            break

    return PaperMetadata(
        identifier=parsed.raw,
        source=PaperSource.CROSSREF,
        title=title,
        authors=authors,
        abstract=abstract,
        published=_parse_crossref_date(date_parts),
        doi=parsed.value,
        url=f"https://doi.org/{parsed.value}",
        references_count=payload.get("reference-count"),
    )


def _strip_jats(text: str) -> str:
    import re

    return re.sub(r"<[^>]+>", "", text).strip()
