from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import QualitySignal
from peerlens.services.signals.artifacts import ArtifactAvailabilityChecker
from peerlens.services.signals.base import SignalChecker
from peerlens.services.signals.metadata import MetadataCompletenessChecker
from peerlens.services.signals.retraction import RetractionChecker

DEFAULT_CHECKERS: list[SignalChecker] = [
    MetadataCompletenessChecker(),
    RetractionChecker(),
    ArtifactAvailabilityChecker(),
]


def run_signal_checks(
    context: AnalysisContext,
    checkers: list[SignalChecker] | None = None,
) -> list[QualitySignal]:
    checkers = checkers or DEFAULT_CHECKERS
    signals: list[QualitySignal] = []
    for checker in checkers:
        signals.extend(checker.check(context))
    return signals
