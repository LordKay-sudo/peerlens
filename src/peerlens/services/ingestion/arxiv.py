from datetime import datetime
from html import unescape
import re

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


def _extract_entry(xml: str) -> str:
    match = re.search(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    return match.group(1) if match else ""


def _extract_tag(xml: str, tag: str, attr: str | None = None) -> str:
    if attr:
        pattern = rf'<{tag}[^>]*{attr}="([^"]+)"'
        match = re.search(pattern, xml)
        return match.group(1).strip() if match else ""

    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    match = re.search(pattern, xml, re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_entry_authors(entry: str) -> list[str]:
    authors: list[str] = []
    for author_block in re.findall(r"<author>(.*?)</author>", entry, re.DOTALL):
        name = _extract_tag(author_block, "name")
        if name:
            authors.append(_clean_text(name))
    return authors


def _extract_entry_categories(entry: str) -> list[str]:
    return re.findall(r'<category[^>]*term="([^"]+)"', entry)


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value)).strip()


def parse_arxiv_atom(xml: str) -> PaperMetadata:
    """Parse an arXiv Atom API response into paper metadata."""
    entry = _extract_entry(xml)
    if not entry:
        raise IngestionError("No arXiv entry found in API response")

    title = _clean_text(_extract_tag(entry, "title"))
    if not title or title.lower().startswith("arxiv query:"):
        raise IngestionError("Could not parse paper title from arXiv response")

    abstract = _clean_text(_extract_tag(entry, "summary")) or None
    published = _extract_tag(entry, "published")
    arxiv_id_match = re.search(r"<id>https?://arxiv\.org/abs/([^<]+)</id>", entry)
    arxiv_id = arxiv_id_match.group(1).split("v")[0] if arxiv_id_match else "unknown"

    return PaperMetadata(
        identifier=arxiv_id,
        source=PaperSource.ARXIV,
        title=title,
        authors=_extract_entry_authors(entry),
        abstract=abstract,
        published=_parse_arxiv_date(published),
        url=f"https://arxiv.org/abs/{arxiv_id}",
        keywords=_extract_entry_categories(entry),
    )


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

    paper = parse_arxiv_atom(text)
    return paper.model_copy(update={"identifier": parsed.raw})
