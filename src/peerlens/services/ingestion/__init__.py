from peerlens.config import Settings
from peerlens.core.exceptions import IdentifierError, IngestionError
from peerlens.models.schemas import PaperMetadata
from peerlens.services.ingestion.arxiv import fetch_from_arxiv
from peerlens.services.ingestion.crossref import fetch_from_crossref
from peerlens.services.ingestion.identifiers import parse_identifier


async def ingest_paper(identifier: str, settings: Settings | None = None) -> PaperMetadata:
    try:
        parsed = parse_identifier(identifier)
    except IdentifierError:
        raise

    if parsed.kind == "arxiv":
        return await fetch_from_arxiv(parsed, settings=settings)
    if parsed.kind == "doi":
        return await fetch_from_crossref(parsed, settings=settings)

    raise IngestionError(f"Unsupported source kind: {parsed.kind}")
