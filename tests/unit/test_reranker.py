from src.rag.reranker import DocumentReranker


def test_reranker():

    docs = [
        {"id": 1},
        {"id": 2},
    ]

    result = DocumentReranker().rerank(
        "vpn",
        docs,
        top_k=1,
    )

    assert len(result) == 1
