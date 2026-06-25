from peerlens.models.schemas import PaperMetadata, QualitySignal, SignalSeverity
from peerlens.services.signals.base import SignalChecker

_REPRO_KEYWORDS = (
    "code availability",
    "data availability",
    "open data",
    "open-source",
    "open source",
    "reproducib",
    "supplementary material",
    "github.com",
    "zenodo",
    "figshare",
    "osf.io",
)


class ReproducibilityHintsChecker(SignalChecker):
    id = "reproducibility_hints"
    name = "Reproducibility hints"
    dimension = "reproducibility"

    def check(self, paper: PaperMetadata) -> list[QualitySignal]:
        text = " ".join(
            filter(
                None,
                [paper.abstract or "", paper.title, " ".join(paper.keywords)],
            )
        ).lower()

        hits = [kw for kw in _REPRO_KEYWORDS if kw in text]
        if hits:
            return [
                QualitySignal(
                    id="repro_hints_found",
                    name="Reproducibility signals detected",
                    severity=SignalSeverity.INFO,
                    message="Text mentions artifacts or reproducibility-related terms.",
                    evidence=", ".join(sorted(set(hits))),
                    dimension=self.dimension,
                )
            ]

        return [
            QualitySignal(
                id="no_repro_hints",
                name="No reproducibility hints in metadata",
                severity=SignalSeverity.INFO,
                message=(
                    "Abstract/metadata does not mention code, data, or supplementary materials. "
                    "This is not evidence of poor quality — only that openness cannot be inferred yet."
                ),
                dimension=self.dimension,
            )
        ]
