from abc import ABC, abstractmethod

from peerlens.models.schemas import PaperMetadata, QualitySignal


class SignalChecker(ABC):
    id: str
    name: str
    dimension: str

    @abstractmethod
    def check(self, paper: PaperMetadata) -> list[QualitySignal]:
        pass
