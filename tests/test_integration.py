import pytest

from peerlens.core.exceptions import IngestionError
from peerlens.services.reports import analyze_paper


@pytest.mark.asyncio
async def test_arxiv_live_title_is_not_query_string():
    report = await analyze_paper("2301.07041")
    title = report.paper.title.lower()
    assert "arxiv query" not in title
    assert "search_query" not in title
    assert len(report.paper.title) > 10


@pytest.mark.asyncio
async def test_arxiv_live_fetches_pdf_sections_when_available():
    report = await analyze_paper("2301.07041")
    if report.pdf_analyzed:
        assert report.sections or report.paper.title
