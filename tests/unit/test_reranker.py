from src.rag.reranker import DocumentReranker


def test_reranker():

    docs = [
        {
            "id": 1,
            "content": "VPN configuration guide",
            "score": 1.5,
        },
        {
            "id": 2,
            "content": "Printer setup guide",
            "score": 2.0,
        },
    ]

    result = DocumentReranker().rerank(
        "vpn",
        docs,
    )

    assert result[0]["id"] == 1
