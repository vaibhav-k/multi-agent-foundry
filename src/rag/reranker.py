"""
Document reranking utilities.

Improves retrieval quality by selecting the
most relevant chunks.
"""


class DocumentReranker:
    """
    Selects the best documents from search results.
    """

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Return top ranked documents.

        Current implementation assumes search
        already returned ranked results.
        """

        return documents[:top_k]
