"""
Query transformation utilities.

Improves user questions before sending them
to Azure AI Search.
"""


class QueryRewriter:
    """
    Converts natural language questions into
    search-optimized queries.
    """

    def rewrite(
        self,
        question: str,
    ) -> str:
        """
        Create an optimized search query.

        Current implementation keeps the query unchanged.
        Replace with LLM-based rewriting later.
        """

        return question.strip()
