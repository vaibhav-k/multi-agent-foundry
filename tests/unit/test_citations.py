from src.rag.citations import CitationBuilder


def test_citations():

    result = CitationBuilder().build([{"source": "vpn.md"}])

    assert result[0].name == "vpn.md"
