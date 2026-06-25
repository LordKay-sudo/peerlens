from peerlens.models.schemas import PaperMetadata, QualitySignal
from peerlens.services.signals.base import SignalChecker
from peerlens.services.signals.metadata import MetadataCompletenessChecker
from peerlens.services.signals.reproducibility import ReproducibilityHintsChecker

DEFAULT_CHECKERS: list[SignalChecker] = [
    MetadataCompletenessChecker(),
    ReproducibilityHintsChecker(),
]


def run_signal_checks(paper: PaperMetadata, checkers: list[SignalChecker] | None = None) -> list[QualitySignal]:
    checkers = checkers or DEFAULT_CHECKERS
    signals: list[QualitySignal] = []
    for checker in checkers:
        signals.extend(checker.check(paper))
    return signals
