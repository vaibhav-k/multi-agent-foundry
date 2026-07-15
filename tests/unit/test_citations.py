from src.rag.citations import CitationBuilder


def test_citations():

    result = CitationBuilder().build([{"source": "vpn.md"}])

    assert result[0].name == "vpn.md"


def test_duplicate_citations_are_removed():

    builder = CitationBuilder()

    documents = [
        {
            "source": "vpn.md",
            "score": 4.5,
        },
        {
            "source": "vpn.md",
            "score": 4.2,
        },
        {
            "source": "mfa_setup.md",
            "score": 4.0,
        },
    ]

    result = builder.build(documents)

    assert len(result) == 2
    assert result[0].name == "vpn.md"
    assert result[1].name == "mfa_setup.md"
