from dataclasses import dataclass, field
from typing import Any

from peerlens.models.schemas import PaperMetadata


@dataclass
class AnalysisContext:
    paper: PaperMetadata
    full_text: str | None = None
    sections: dict[str, str] = field(default_factory=dict)
    pdf_analyzed: bool = False
    crossref_record: dict[str, Any] | None = None

    @property
    def searchable_text(self) -> str:
        parts = [self.paper.title, self.paper.abstract or ""]
        if self.full_text:
            parts.append(self.full_text)
        return "\n".join(parts)
