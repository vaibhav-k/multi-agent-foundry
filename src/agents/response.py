"""
Response generation agent.

Creates the final user-facing answer from
retrieved knowledge and validation results.
"""


class ResponseAgent:
    """
    Generates final assistant responses.
    """

    def generate(
        self,
        answer: str,
        sources: list[str],
    ) -> dict:

        return {
            "answer": answer,
            "sources": sources,
        }
