import pytest

from peerlens.core.exceptions import IdentifierError
from peerlens.services.ingestion.identifiers import parse_identifier


def test_parse_arxiv_id():
    parsed = parse_identifier("2301.07041")
    assert parsed.kind == "arxiv"
    assert parsed.value == "2301.07041"


def test_parse_doi():
    parsed = parse_identifier("10.1038/nature12373")
    assert parsed.kind == "doi"
    assert parsed.value == "10.1038/nature12373"


def test_parse_arxiv_url():
    parsed = parse_identifier("https://arxiv.org/abs/2301.07041v2")
    assert parsed.kind == "arxiv"
    assert parsed.value == "2301.07041v2"


def test_invalid_identifier():
    with pytest.raises(IdentifierError):
        parse_identifier("not-a-real-id")
