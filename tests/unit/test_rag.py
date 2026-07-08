from src.rag.validators import validate_context


def test_context_validation():

    assert validate_context([{"content": "VPN setup"}])

    assert not validate_context([])
