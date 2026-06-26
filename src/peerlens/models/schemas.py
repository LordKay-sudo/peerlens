from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class SignalSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CONCERN = "concern"


class PaperSource(StrEnum):
    ARXIV = "arxiv"
    CROSSREF = "crossref"
    UPLOAD = "upload"


class QualitySignal(BaseModel):
    id: str
    name: str
    severity: SignalSeverity
    message: str
    evidence: str | None = None
    dimension: str = "general"


class PaperMetadata(BaseModel):
    identifier: str
    source: PaperSource
    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str | None = None
    published: datetime | None = None
    doi: str | None = None
    url: HttpUrl | None = None
    keywords: list[str] = Field(default_factory=list)
    references_count: int | None = None
    sections: dict[str, str] = Field(default_factory=dict)
    pdf_analyzed: bool = False


class QualityReport(BaseModel):
    identifier: str
    paper: PaperMetadata
    signals: list[QualitySignal] = Field(default_factory=list)
    summary: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sections: dict[str, str] = Field(default_factory=dict)
    pdf_analyzed: bool = False


class AnalyzeRequest(BaseModel):
    identifier: str = Field(
        ...,
        description="DOI (10.xxx/...), arXiv ID (2301.00001 or arxiv:2301.00001), or URL",
        examples=["10.1038/nature12373", "2301.00001"],
    )


class HealthResponse(BaseModel):
    status: str
    version: str


class AskRequest(BaseModel):
    identifier: str = Field(..., description="Same identifier used for analysis")
    question: str = Field(..., min_length=3, max_length=1000)
    top_k: int | None = Field(default=None, ge=1, le=10)


class CitationSpan(BaseModel):
    index: int
    section: str | None = None
    excerpt: str
    score: float


class AskResponse(BaseModel):
    identifier: str
    question: str
    answer: str
    citations: list[CitationSpan] = Field(default_factory=list)
    model: str | None = None
    chunks_used: int = 0
    pdf_analyzed: bool = False
