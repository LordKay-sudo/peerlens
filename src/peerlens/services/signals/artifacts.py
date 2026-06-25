import re

from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import QualitySignal, SignalSeverity
from peerlens.services.signals.base import SignalChecker

ARTIFACT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("GitHub", re.compile(r"https?://(?:www\.)?github\.com/[^\s)>\"]+", re.I)),
    ("Zenodo", re.compile(r"https?://(?:www\.)?zenodo\.org/[^\s)>\"]+", re.I)),
    ("Figshare", re.compile(r"https?://(?:www\.)?figshare\.com/[^\s)>\"]+", re.I)),
    ("OSF", re.compile(r"https?://(?:www\.)?osf\.io/[^\s)>\"]+", re.I)),
    ("Dryad", re.compile(r"https?://(?:datadryad\.org|doi\.org/10\.5061)/[^\s)>\"]+", re.I)),
    ("Hugging Face", re.compile(r"https?://(?:www\.)?huggingface\.co/[^\s)>\"]+", re.I)),
]

ARTIFACT_PHRASES = (
    "code availability",
    "data availability",
    "supplementary material",
    "open data",
    "open-source",
    "open source",
    "source code",
)


class ArtifactAvailabilityChecker(SignalChecker):
    id = "artifact_availability"
    name = "Code & data artifacts"
    dimension = "reproducibility"

    def check(self, context: AnalysisContext) -> list[QualitySignal]:
        text = context.searchable_text
        found: dict[str, str] = {}

        for label, pattern in ARTIFACT_PATTERNS:
            match = pattern.search(text)
            if match:
                found[label] = match.group(0).rstrip(".,;)]")

        if found:
            evidence = "; ".join(f"{label}: {url}" for label, url in found.items())
            return [
                QualitySignal(
                    id="artifacts_found",
                    name="Research artifacts linked",
                    severity=SignalSeverity.INFO,
                    message=(
                        "Found links to code or data repositories in the analyzed text. "
                        "Verify they resolve and match this paper."
                    ),
                    evidence=evidence[:500],
                    dimension=self.dimension,
                )
            ]

        phrase_hits = [phrase for phrase in ARTIFACT_PHRASES if phrase in text.lower()]
        if phrase_hits and not found:
            return [
                QualitySignal(
                    id="artifact_claim_without_link",
                    name="Availability mentioned without repository link",
                    severity=SignalSeverity.WARNING,
                    message=(
                        "Text mentions data/code availability but no common repository URL "
                        "was detected (GitHub, Zenodo, OSF, Figshare, Dryad, Hugging Face)."
                    ),
                    evidence=", ".join(phrase_hits),
                    dimension=self.dimension,
                )
            ]

        if context.sections.get("methods") and not found:
            return [
                QualitySignal(
                    id="methods_without_artifacts",
                    name="Methods section without artifact links",
                    severity=SignalSeverity.WARNING,
                    message=(
                        "A methods section was extracted from the PDF, but no standard "
                        "code/data repository links were found."
                    ),
                    dimension=self.dimension,
                )
            ]

        if not context.pdf_analyzed:
            return [
                QualitySignal(
                    id="metadata_only_scan",
                    name="Metadata-only artifact scan",
                    severity=SignalSeverity.INFO,
                    message=(
                        "Artifact check ran on title/abstract only. Upload a PDF or use an "
                        "arXiv ID for full-text repository link detection."
                    ),
                    dimension=self.dimension,
                )
            ]

        return [
            QualitySignal(
                id="no_artifacts_found",
                name="No artifact links detected",
                severity=SignalSeverity.INFO,
                message=(
                    "Full text was analyzed but no standard repository links were found. "
                    "Artifacts may still exist under other hosts or in supplementary files."
                ),
                dimension=self.dimension,
            )
        ]
