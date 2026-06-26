from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import PaperMetadata, PaperSource
from peerlens.services.rag.chunking import TextChunk, build_chunks
from peerlens.services.rag.retrieval import cosine_similarity, retrieve_top_chunks


def test_build_chunks_from_sections():
    paper = PaperMetadata(identifier="x", source=PaperSource.ARXIV, title="Test")
    context = AnalysisContext(
        paper=paper,
        sections={
            "abstract": "We study homomorphic encryption accelerators in depth.",
            "methods": "We benchmark FHE schemes on CPU and FPGA targets.",
            "results": "Our design improves throughput by 3x over prior art.",
        },
        pdf_analyzed=True,
    )
    chunks = build_chunks(context, chunk_size=50, overlap=5)
    sections = {chunk.section for chunk in chunks}
    assert "methods" in sections
    assert "results" in sections


def test_cosine_similarity_identical_vectors():
    vector = [1.0, 0.0, 0.0]
    assert cosine_similarity(vector, vector) == 1.0


def test_retrieve_top_chunks_orders_by_similarity():
    chunks = [
        TextChunk(index=0, text="encryption hardware benchmark", section="methods"),
        TextChunk(index=1, text="related work in graph theory", section="introduction"),
    ]
    embeddings = [
        [1.0, 0.0],
        [0.0, 1.0],
    ]
    query = [0.9, 0.1]
    top = retrieve_top_chunks(chunks, embeddings, query, top_k=1)
    assert top[0][0].section == "methods"
    assert top[0][1] > 0.5
