from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import RAGError
from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import AskResponse, CitationSpan
from peerlens.services.rag.cache import get_analysis_context
from peerlens.services.rag.chunking import build_chunks
from peerlens.services.rag.llm import OpenAIClient
from peerlens.services.rag.retrieval import retrieve_top_chunks

SYSTEM_PROMPT = """You are PeerLens, a careful research assistant.
Answer the user's question using ONLY the provided paper excerpts.
Rules:
- If the excerpts do not contain enough information, say you cannot determine that from the available text.
- Do not invent citations, numbers, or claims.
- Mention which section an point comes from when possible (abstract, methods, results, etc.).
- Be concise but precise. Use plain language.
"""


def _format_excerpts(matches: list[tuple]) -> str:
    lines: list[str] = []
    for chunk, score in matches:
        label = chunk.section or "body"
        lines.append(f"[{chunk.index + 1}] ({label}, relevance={score:.2f})\n{chunk.text}")
    return "\n\n".join(lines)


async def ask_paper(
    identifier: str,
    question: str,
    top_k: int | None = None,
    settings: Settings | None = None,
) -> AskResponse:
    settings = settings or get_settings()
    question = question.strip()
    if not question:
        raise RAGError("Question cannot be empty")

    context = await get_analysis_context(identifier)
    return await ask_context(context, identifier, question, top_k=top_k, settings=settings)


async def ask_context(
    context: AnalysisContext,
    identifier: str,
    question: str,
    top_k: int | None = None,
    settings: Settings | None = None,
) -> AskResponse:
    settings = settings or get_settings()
    top_k = top_k or settings.rag_top_k

    chunks = build_chunks(
        context,
        chunk_size=settings.rag_chunk_size,
        overlap=settings.rag_chunk_overlap,
    )
    if not chunks:
        raise RAGError(
            "No analyzable text found. Use an arXiv ID (auto PDF) or upload a PDF first."
        )

    client = OpenAIClient(settings=settings)
    chunk_embeddings = await client.embed([chunk.text for chunk in chunks])
    query_embedding = (await client.embed([question]))[0]
    matches = retrieve_top_chunks(chunks, chunk_embeddings, query_embedding, top_k=top_k)

    user_prompt = (
        f"Paper title: {context.paper.title}\n\n"
        f"Excerpts:\n{_format_excerpts(matches)}\n\n"
        f"Question: {question}"
    )
    answer = await client.complete(SYSTEM_PROMPT, user_prompt)

    citations = [
        CitationSpan(
            index=chunk.index,
            section=chunk.section,
            excerpt=chunk.text[:400],
            score=round(score, 4),
        )
        for chunk, score in matches
    ]

    return AskResponse(
        identifier=identifier,
        question=question,
        answer=answer,
        citations=citations,
        model=settings.llm_model,
        chunks_used=len(citations),
        pdf_analyzed=context.pdf_analyzed,
    )
