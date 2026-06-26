from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import IngestionError
from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import PaperMetadata, PaperSource, QualityReport, SignalSeverity
from peerlens.services.ingestion import ingest_paper
from peerlens.services.ingestion.crossref import fetch_crossref_record
from peerlens.services.ingestion.identifiers import parse_identifier
from peerlens.services.ingestion.pdf import process_pdf
from peerlens.services.ingestion.pdf_fetch import fetch_arxiv_pdf
from peerlens.services.rag.cache import cache_context
from peerlens.services.signals import run_signal_checks


def _build_summary(signals: list) -> str:
    if not signals:
        return "No quality signals were generated."

    concerns = sum(1 for s in signals if s.severity == SignalSeverity.CONCERN)
    warnings = sum(1 for s in signals if s.severity == SignalSeverity.WARNING)

    if concerns:
        return f"Report includes {concerns} concern(s) and {warnings} warning(s) across {len(signals)} signal(s)."
    if warnings:
        return f"Report includes {warnings} warning(s) across {len(signals)} signal(s)."
    return f"Report includes {len(signals)} informational signal(s); no warnings or concerns from automated checks."


async def _attach_pdf(context: AnalysisContext, pdf_bytes: bytes) -> None:
    full_text, sections = process_pdf(pdf_bytes)
    context.full_text = full_text
    context.sections = sections
    context.pdf_analyzed = True


async def _maybe_fetch_arxiv_pdf(context: AnalysisContext, settings: Settings) -> None:
    if not settings.fetch_arxiv_pdf or context.paper.source != PaperSource.ARXIV:
        return

    parsed = parse_identifier(context.paper.identifier)
    if parsed.kind != "arxiv":
        return

    try:
        pdf_bytes = await fetch_arxiv_pdf(parsed.value, settings=settings)
        await _attach_pdf(context, pdf_bytes)
    except IngestionError:
        return


async def _load_crossref_record(context: AnalysisContext, settings: Settings) -> None:
    if not context.paper.doi:
        return
    try:
        context.crossref_record = await fetch_crossref_record(context.paper.doi, settings=settings)
    except IngestionError:
        context.crossref_record = None


async def build_analysis_context(
    identifier: str,
    pdf_bytes: bytes | None = None,
    settings: Settings | None = None,
) -> AnalysisContext:
    settings = settings or get_settings()
    paper = await ingest_paper(identifier, settings=settings)
    context = AnalysisContext(paper=paper)

    if pdf_bytes is not None:
        await _attach_pdf(context, pdf_bytes)
    else:
        await _maybe_fetch_arxiv_pdf(context, settings)

    if context.paper.doi and context.crossref_record is None:
        await _load_crossref_record(context, settings)
    elif context.paper.source == PaperSource.CROSSREF and context.paper.doi:
        await _load_crossref_record(context, settings)

    return context


async def analyze_paper(identifier: str, pdf_bytes: bytes | None = None) -> QualityReport:
    context = await build_analysis_context(identifier, pdf_bytes=pdf_bytes)
    cache_context(identifier, context)
    signals = run_signal_checks(context)
    paper = context.paper.model_copy(
        update={"sections": context.sections, "pdf_analyzed": context.pdf_analyzed}
    )
    return QualityReport(
        identifier=identifier,
        paper=paper,
        signals=signals,
        summary=_build_summary(signals),
        sections=context.sections,
        pdf_analyzed=context.pdf_analyzed,
    )


async def analyze_uploaded_pdf(filename: str, pdf_bytes: bytes) -> QualityReport:
    settings = get_settings()
    if len(pdf_bytes) > settings.max_upload_bytes:
        raise IngestionError(
            f"PDF exceeds upload limit ({settings.max_upload_bytes // (1024 * 1024)} MB)"
        )

    full_text, sections = process_pdf(pdf_bytes)
    title = _title_from_pdf_text(full_text) or filename.removesuffix(".pdf")
    paper = PaperMetadata(
        identifier=f"upload:{filename}",
        source=PaperSource.UPLOAD,
        title=title,
        abstract=sections.get("abstract") or _first_paragraph(full_text),
        pdf_analyzed=True,
        sections=sections,
    )
    context = AnalysisContext(
        paper=paper,
        full_text=full_text,
        sections=sections,
        pdf_analyzed=True,
    )
    cache_context(paper.identifier, context)
    signals = run_signal_checks(context)
    return QualityReport(
        identifier=paper.identifier,
        paper=paper,
        signals=signals,
        summary=_build_summary(signals),
        sections=sections,
        pdf_analyzed=True,
    )


def _first_paragraph(text: str) -> str | None:
    for block in text.split("\n\n"):
        cleaned = " ".join(block.split())
        if len(cleaned) >= 80:
            return cleaned[:1200]
    return None


def _title_from_pdf_text(text: str) -> str | None:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:8]:
        if 12 <= len(line) <= 180 and line.lower() not in {"abstract", "introduction"}:
            return line
    return None
