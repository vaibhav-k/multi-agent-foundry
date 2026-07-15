from src.rag.query import QueryRewriter


def test_query_rewrite_removes_whitespace():

    result = QueryRewriter().rewrite("   \t How do I setup VPN?   \t ")

    assert result == ("How do i setup VPN virtual private network?")


def test_query_rewrite_removes_filler():

    result = QueryRewriter().rewrite("Can you please tell me how to setup MFA?")

    assert "can you" not in result and "please" not in result


def test_query_rewrite_expands_terms():

    result = QueryRewriter().rewrite("How do I configure SSO?")

    assert "SSO single sign on" in result


def test_empty_query_returns_empty_string():

    result = QueryRewriter().rewrite("")

    assert result == ""
