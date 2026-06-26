from dataclasses import dataclass
import re

from peerlens.models.context import AnalysisContext


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    section: str | None = None


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(words):
            break
        start = max(0, end - overlap)
    return chunks


def build_chunks(
    context: AnalysisContext,
    chunk_size: int = 900,
    overlap: int = 120,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    index = 0

    if context.paper.abstract:
        for part in _split_long_text(context.paper.abstract, chunk_size, overlap):
            chunks.append(TextChunk(index=index, text=part, section="abstract"))
            index += 1

    if context.sections:
        for section_name, body in context.sections.items():
            if section_name == "abstract":
                continue
            for part in _split_long_text(body, chunk_size, overlap):
                chunks.append(TextChunk(index=index, text=part, section=section_name))
                index += 1
        if chunks:
            return chunks

    source_text = context.full_text or ""
    if not source_text:
        return chunks

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", source_text) if p.strip()]
    buffer = ""
    for paragraph in paragraphs:
        candidate = f"{buffer} {paragraph}".strip() if buffer else paragraph
        if len(candidate.split()) <= chunk_size:
            buffer = candidate
            continue
        if buffer:
            chunks.append(TextChunk(index=index, text=buffer, section=None))
            index += 1
        for part in _split_long_text(paragraph, chunk_size, overlap):
            chunks.append(TextChunk(index=index, text=part, section=None))
            index += 1
        buffer = ""

    if buffer:
        chunks.append(TextChunk(index=index, text=buffer, section=None))

    return chunks
