"""
RAG context validation.
"""


def validate_context(
    documents: list,
) -> bool:
    """
    Check retrieved documents exist.
    """

    if not documents:
        return False

    for doc in documents:
        if doc.get("content"):
            return True

    return False
