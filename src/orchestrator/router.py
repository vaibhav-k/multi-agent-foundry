"""
Agent routing decisions.
"""


class AgentRouter:
    """
    Determines required agent execution path.
    """

    def requires_knowledge(
        self,
        intent: str | None,
    ) -> bool:

        return intent in {
            "question",
            "policy",
            "procedure",
        }
