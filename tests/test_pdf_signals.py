from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import PaperMetadata, PaperSource, SignalSeverity
from peerlens.services.ingestion.pdf import extract_sections
from peerlens.services.signals.artifacts import ArtifactAvailabilityChecker
from peerlens.services.signals.retraction import RetractionChecker, _is_retracted

SAMPLE_SECTION_TEXT = """
Abstract
This paper studies reproducible workflows.

Introduction
We motivate the problem.

Methods
We trained models on public data hosted at https://github.com/example/research-code.

Results
Accuracy improved by twelve points over the baseline on all held-out evaluation splits.

Discussion
Future work remains.
"""


def test_extract_sections_finds_methods_and_results():
    sections = extract_sections(SAMPLE_SECTION_TEXT)
    assert "methods" in sections
    assert "results" in sections
    assert "github.com" in sections["methods"]


def test_artifact_checker_finds_github_link():
    paper = PaperMetadata(
        identifier="test",
        source=PaperSource.UPLOAD,
        title="Test",
        pdf_analyzed=True,
    )
    context = AnalysisContext(
        paper=paper,
        full_text=SAMPLE_SECTION_TEXT,
        sections=extract_sections(SAMPLE_SECTION_TEXT),
        pdf_analyzed=True,
    )
    signals = ArtifactAvailabilityChecker().check(context)
    assert any(signal.id == "artifacts_found" for signal in signals)


def test_retraction_checker_flags_crossref_retraction():
    paper = PaperMetadata(
        identifier="10.1234/example",
        source=PaperSource.CROSSREF,
        title="Example",
        doi="10.1234/example",
    )
    record = {
        "title": ["Example paper"],
        "update-to": [{"type": "retraction", "label": "Retraction notice"}],
    }
    context = AnalysisContext(paper=paper, crossref_record=record)
    signals = RetractionChecker().check(context)
    assert any(signal.severity == SignalSeverity.CONCERN for signal in signals)


def test_is_retracted_detects_relation():
    retracted, evidence = _is_retracted(
        {"relation": [{"type": "is-retracted-by", "id": "10.5555/retraction"}]}
    )
    assert retracted is True
    assert evidence is not None
