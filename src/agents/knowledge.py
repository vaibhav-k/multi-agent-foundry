"""
Knowledge Agent.

Responsible for answering user questions using
enterprise knowledge sources.

Future enhancements:
- Azure AI Search retrieval
- Vector search
- Document chunk ranking
- Citation generation
"""

from typing import Optional

from src.agents.base import BaseAgent
from src.config import get_logger

logger = get_logger(__name__)


class KnowledgeAgent(BaseAgent):
    """
    Knowledge retrieval and answer generation agent.

    Current capability:
    - Generate answers using model knowledge

    Future capability:
    - Generate grounded answers using RAG context
    """

    def __init__(self):

        super().__init__(
            name="KnowledgeAgent",
            prompt_file="knowledge.txt",
        )

    def answer(
        self,
        user_input: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Generate an answer using available knowledge.

        Args:
            user_input:
                User question.

            context:
                Retrieved enterprise documents.

        Returns:
            Generated answer.
        """

        logger.info("KnowledgeAgent answering request")

        return super().run(
            user_input=user_input,
            context=context,
        )
