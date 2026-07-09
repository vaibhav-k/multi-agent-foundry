"""
RAG evaluation helpers.

Provides lightweight quality checks
for retrieved responses.
"""


class RAGEvaluator:
    """
    Evaluates retrieval quality.
    """

    def contains_source(
        self,
        sources: list[str],
        expected: str,
    ) -> bool:

        return expected in sources
