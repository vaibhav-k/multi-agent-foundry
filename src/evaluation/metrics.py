"""
Evaluation metrics for RAG quality.
"""


def retrieval_accuracy(
    expected: str,
    actual: list[str],
) -> float:
    """
    Calculate simple retrieval accuracy.
    """

    return 1.0 if expected in actual else 0.0
