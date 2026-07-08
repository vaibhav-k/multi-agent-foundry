"""
Knowledge Agent.

Uses enterprise retrieval and generates grounded answers.
"""

from typing import Optional

from src.agents.base import BaseAgent
from src.config import get_logger
from src.rag import RAGPipeline

logger = get_logger(__name__)


class KnowledgeAgent(BaseAgent):
    """
    Enterprise knowledge retrieval agent.

    Flow:

    User question
        |
    Azure AI Search
        |
    Retrieved context
        |
    LLM response
    """

    def __init__(self):

        super().__init__(
            name="KnowledgeAgent",
            prompt_file="knowledge.txt",
        )

        self.rag = RAGPipeline()

    def answer(
        self,
        user_input: str,
        context: Optional[str] = None,
    ) -> str:

        logger.info("KnowledgeAgent processing request")

        if not context:

            documents = self.rag.retrieve(user_input)

            context = self.rag.build_context(documents)

        return self.run(
            user_input=user_input,
            context=context,
        )

    def run(
        self,
        user_input: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Execute knowledge workflow.
        """

        prompt = f"""
    Context:
    {context or "No enterprise context available."}


    Question:
    {user_input}


    Answer using only the context above.
    """

        return super().run(user_input=prompt)
