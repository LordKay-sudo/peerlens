from peerlens.models.schemas import QualityReport, SignalSeverity
from peerlens.services.ingestion import ingest_paper
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


async def analyze_paper(identifier: str) -> QualityReport:
    paper = await ingest_paper(identifier)
    signals = run_signal_checks(paper)
    return QualityReport(
        identifier=identifier,
        paper=paper,
        signals=signals,
        summary=_build_summary(signals),
    )
