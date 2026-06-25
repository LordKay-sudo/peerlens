import re
from dataclasses import dataclass

from peerlens.core.exceptions import IdentifierError


@dataclass(frozen=True)
class ParsedIdentifier:
    raw: str
    kind: str  # "doi" | "arxiv"
    value: str


_ARXIV_PATTERNS = [
    re.compile(r"^arxiv:(?P<id>\d{4}\.\d{4,5}(?:v\d+)?)$", re.I),
    re.compile(r"^(?P<id>\d{4}\.\d{4,5}(?:v\d+)?)$"),
    re.compile(r"arxiv\.org/abs/(?P<id>\d{4}\.\d{4,5}(?:v\d+)?)", re.I),
]

_DOI_PATTERNS = [
    re.compile(r"^doi:(?P<doi>10\.\d{4,9}/\S+)$", re.I),
    re.compile(r"^(?P<doi>10\.\d{4,9}/\S+)$", re.I),
    re.compile(r"doi\.org/(?P<doi>10\.\d{4,9}/\S+)", re.I),
]


def parse_identifier(raw: str) -> ParsedIdentifier:
    value = raw.strip()
    if not value:
        raise IdentifierError("Identifier cannot be empty")

    for pattern in _ARXIV_PATTERNS:
        match = pattern.search(value)
        if match:
            arxiv_id = match.group("id")
            return ParsedIdentifier(raw=raw, kind="arxiv", value=arxiv_id)

    for pattern in _DOI_PATTERNS:
        match = pattern.search(value)
        if match:
            doi = match.group("doi").rstrip(".,)")
            return ParsedIdentifier(raw=raw, kind="doi", value=doi)

    raise IdentifierError(
        f"Unsupported identifier: {raw!r}. Use a DOI (10.xxx/...) or arXiv ID (YYYY.NNNNN)."
    )
