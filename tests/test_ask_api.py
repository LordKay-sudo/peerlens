import pytest
from httpx import ASGITransport, AsyncClient

from peerlens.main import create_app
from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import PaperMetadata, PaperSource


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_ask_without_api_key_returns_demo_message(client, monkeypatch):
    async def fake_context(identifier: str) -> AnalysisContext:
        return AnalysisContext(
            paper=PaperMetadata(
                identifier=identifier,
                source=PaperSource.ARXIV,
                title="Sample paper",
                abstract="This paper benchmarks homomorphic encryption on CPUs and FPGAs.",
            ),
            full_text="Methods include benchmarking and hardware synthesis.",
            pdf_analyzed=True,
        )

    monkeypatch.setattr("peerlens.services.rag.qa.get_analysis_context", fake_context)

    response = await client.post(
        "/api/v1/papers/ask",
        json={"identifier": "2301.07041", "question": "What methods are used?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["demo_mode"] is True
    assert "demo version" in payload["answer"].lower()
    assert payload["citations"] == []


@pytest.mark.asyncio
async def test_health_reports_demo_mode_without_api_key(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["rag_demo_mode"] is True
