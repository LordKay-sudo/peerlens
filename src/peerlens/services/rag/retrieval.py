import math

from peerlens.services.rag.chunking import TextChunk


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def retrieve_top_chunks(
    chunks: list[TextChunk],
    chunk_embeddings: list[list[float]],
    query_embedding: list[float],
    top_k: int,
) -> list[tuple[TextChunk, float]]:
    scored: list[tuple[TextChunk, float]] = []
    for chunk, embedding in zip(chunks, chunk_embeddings, strict=True):
        scored.append((chunk, cosine_similarity(query_embedding, embedding)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]
