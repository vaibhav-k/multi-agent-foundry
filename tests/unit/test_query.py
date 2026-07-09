from src.rag.query import QueryRewriter


def test_query_rewrite():

    result = QueryRewriter().rewrite("How do I setup VPN?")

    assert result == "How do I setup VPN?"
