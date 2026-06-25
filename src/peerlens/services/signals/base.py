from abc import ABC, abstractmethod

from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import QualitySignal


class SignalChecker(ABC):
    id: str
    name: str
    dimension: str

    @abstractmethod
    def check(self, context: AnalysisContext) -> list[QualitySignal]:
        pass
