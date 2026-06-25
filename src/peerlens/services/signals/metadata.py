from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import QualitySignal, SignalSeverity
from peerlens.services.signals.base import SignalChecker


class MetadataCompletenessChecker(SignalChecker):
    id = "metadata_completeness"
    name = "Metadata completeness"
    dimension = "metadata"

    def check(self, context: AnalysisContext) -> list[QualitySignal]:
        paper = context.paper
        signals: list[QualitySignal] = []

        if not paper.abstract:
            signals.append(
                QualitySignal(
                    id="missing_abstract",
                    name="Missing abstract",
                    severity=SignalSeverity.WARNING,
                    message="No abstract was available from the metadata source.",
                    dimension=self.dimension,
                )
            )

        if not paper.authors:
            signals.append(
                QualitySignal(
                    id="missing_authors",
                    name="Missing authors",
                    severity=SignalSeverity.WARNING,
                    message="Author list is empty in the fetched metadata.",
                    dimension=self.dimension,
                )
            )

        if paper.published is None:
            signals.append(
                QualitySignal(
                    id="missing_date",
                    name="Missing publication date",
                    severity=SignalSeverity.INFO,
                    message="Publication date could not be determined.",
                    dimension=self.dimension,
                )
            )

        if paper.abstract and len(paper.abstract) < 120:
            signals.append(
                QualitySignal(
                    id="short_abstract",
                    name="Very short abstract",
                    severity=SignalSeverity.INFO,
                    message="Abstract is unusually short; manual review may be needed.",
                    evidence=paper.abstract[:200],
                    dimension=self.dimension,
                )
            )

        return signals
