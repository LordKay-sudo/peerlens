import re
from io import BytesIO

from pypdf import PdfReader

from peerlens.core.exceptions import IngestionError

SECTION_HEADINGS: list[tuple[str, re.Pattern[str]]] = [
    ("abstract", re.compile(r"^\s*(?:\d+\.?\s*)?abstract\s*$", re.I | re.M)),
    ("introduction", re.compile(r"^\s*(?:\d+\.?\s*)?introduction\s*$", re.I | re.M)),
    ("methods", re.compile(r"^\s*(?:\d+\.?\s*)?(?:methods?|materials and methods)\s*$", re.I | re.M)),
    ("results", re.compile(r"^\s*(?:\d+\.?\s*)?results?\s*$", re.I | re.M)),
    ("discussion", re.compile(r"^\s*(?:\d+\.?\s*)?discussion\s*$", re.I | re.M)),
    ("limitations", re.compile(r"^\s*(?:\d+\.?\s*)?limitations?\s*$", re.I | re.M)),
    ("conclusion", re.compile(r"^\s*(?:\d+\.?\s*)?conclusions?\s*$", re.I | re.M)),
    ("references", re.compile(r"^\s*(?:\d+\.?\s*)?references?\s*$", re.I | re.M)),
]


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        raise IngestionError("PDF file is empty")

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as exc:
        raise IngestionError("Could not read PDF file") from exc

    if len(reader.pages) == 0:
        raise IngestionError("PDF has no pages")

    chunks: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            chunks.append(page_text)

    text = "\n".join(chunks).strip()
    if not text:
        raise IngestionError("No extractable text found in PDF (may be scanned images)")

    return re.sub(r"\r\n?", "\n", text)


def extract_sections(text: str) -> dict[str, str]:
    matches: list[tuple[int, str]] = []
    for name, pattern in SECTION_HEADINGS:
        for match in pattern.finditer(text):
            matches.append((match.start(), name))

    if not matches:
        return {}

    matches.sort(key=lambda item: item[0])
    sections: dict[str, str] = {}
    for index, (start, name) in enumerate(matches):
        if name in sections:
            continue
        end = matches[index + 1][0] if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"^\s*(?:\d+\.?\s*)?\w[\w\s]*\s*$", "", body, count=1, flags=re.M).strip()
        if len(body) >= 40:
            sections[name] = body[:8000]

    return sections


def process_pdf(pdf_bytes: bytes) -> tuple[str, dict[str, str]]:
    text = extract_text_from_pdf(pdf_bytes)
    sections = extract_sections(text)
    return text, sections
