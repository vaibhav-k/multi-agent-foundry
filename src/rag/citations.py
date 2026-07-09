"""
Citation generation utilities.

Creates references for grounded responses.
"""

from src.models import DocumentReference


class CitationBuilder:
    """
    Builds document citations.
    """

    def build(
        self,
        documents: list[dict],
    ) -> list[DocumentReference]:

        citations = []

        for document in documents:
            citations.append(
                DocumentReference(
                    name=document.get(
                        "source",
                        "unknown",
                    ),
                    section=document.get("section"),
                    score=document.get("score"),
                )
            )

        return citations
