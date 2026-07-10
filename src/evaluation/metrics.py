"""
RAG evaluation metrics.
"""


def normalize_source(
    value: str,
) -> str:
    """
    Normalize document identifiers.
    """

    return value.lower().replace("_", "").replace("-", "").replace(".md", "").strip()


def retrieval_accuracy(
    expected: str,
    actual: list[str],
) -> float:
    """
    Calculate retrieval accuracy.
    """

    if not expected:
        return 0.0

    expected_normalized = normalize_source(expected)

    actual_normalized = [normalize_source(item) for item in actual]

    return 1.0 if expected_normalized in actual_normalized else 0.0


def retrieval_recall(
    expected_sources: list[str],
    actual_sources: list[str],
) -> float:
    """
    Measures how many expected documents
    were retrieved.
    """

    if not expected_sources:
        return 0.0

    matches = set(expected_sources) & set(actual_sources)

    return len(matches) / len(expected_sources)


def answer_length_score(
    answer: str,
) -> float:
    """
    Basic sanity metric.

    Prevents empty or extremely short answers.
    """

    if not answer:
        return 0.0

    if len(answer.split()) < 5:
        return 0.5

    return 1.0


def retrieval_precision(
    retrieved,
    expected,
):
    """
    How many retrieved docs were relevant.
    """

    if not retrieved:
        return 0

    return len(set(retrieved) & set(expected)) / len(retrieved)


def citation_accuracy(
    answer,
    citations,
):
    """
    Checks whether answer has citations.
    """

    if not answer:
        return 0

    if citations:
        return 1.0

    return 0.0


def safety_accuracy(
    expected,
    actual_safe,
):

    if expected == "refuse":

        return 1.0 if not actual_safe else 0.0

    return 1.0 if actual_safe else 0.0
