from peerlens.core.exceptions import IngestionError
from peerlens.services.ingestion.arxiv import parse_arxiv_atom

SAMPLE_ARXIV_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>arXiv Query: search_query=&amp;id_list=2301.07041&amp;start=0&amp;max_results=10</title>
  <entry>
    <id>https://arxiv.org/abs/2301.07041v1</id>
    <title>SoK: Fully Homomorphic Encryption Accelerators</title>
    <summary>  Sample abstract about FHE accelerators.  </summary>
    <published>2023-01-17T18:59:58Z</published>
    <author><name>Alexander Viand</name></author>
    <author><name>Christian Knabenhans</name></author>
    <category term="cs.CR" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
</feed>
"""


def test_parse_arxiv_atom_uses_entry_title_not_feed_title():
    paper = parse_arxiv_atom(SAMPLE_ARXIV_ATOM)

    assert paper.title == "SoK: Fully Homomorphic Encryption Accelerators"
    assert "arxiv query" not in paper.title.lower()
    assert paper.authors == ["Alexander Viand", "Christian Knabenhans"]
    assert paper.abstract == "Sample abstract about FHE accelerators."
    assert paper.keywords == ["cs.CR"]
    assert str(paper.url) == "https://arxiv.org/abs/2301.07041"


def test_parse_arxiv_atom_rejects_missing_entry():
    try:
        parse_arxiv_atom("<feed><title>arXiv Query</title></feed>")
    except IngestionError:
        pass
    else:
        raise AssertionError("Expected IngestionError")
