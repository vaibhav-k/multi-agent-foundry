"""
Knowledge Agent.

Responsible for enterprise knowledge retrieval and
grounded response generation.

Pipeline:

User Question
      |
Query Rewrite
      |
Azure AI Search Retrieval
      |
Document Reranking
      |
Context Construction
      |
LLM Generation
      |
Citation Builder
      |
Grounded Answer
"""

from typing import Optional

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import (
    DocumentReference,
    GroundedAnswer,
)
from src.rag import (
    RAGBuilder,
    RAGRetriever,
)
from src.rag.citations import CitationBuilder
from src.rag.query import QueryRewriter
from src.rag.reranker import DocumentReranker

logger = get_logger(__name__)


class KnowledgeAgent(BaseAgent):
    """
    Enterprise knowledge retrieval agent.

    Responsibilities:

    - Understand knowledge requests
    - Retrieve enterprise documents
    - Improve retrieval quality
    - Generate grounded answers
    - Provide supporting citations
    """

    def __init__(self):

        super().__init__(
            name="KnowledgeAgent",
            prompt_file="knowledge.txt",
        )

        self.rag = RAGBuilder()

        self.retriever = RAGRetriever()

        self.query_rewriter = QueryRewriter()

        self.reranker = DocumentReranker()

        self.citation_builder = CitationBuilder()

    def answer(
        self,
        user_input: str,
        context: Optional[str] = None,
    ) -> GroundedAnswer:
        """
        Execute the knowledge retrieval pipeline.

        Args:
            user_input:
                Original user question.

            context:
                Optional pre-built context.

        Returns:
            GroundedAnswer containing:
            - answer
            - citations
            - confidence
        """

        logger.info("KnowledgeAgent processing request")

        documents = []

        if context:

            final_context = context

        else:

            search_query = self.query_rewriter.rewrite(user_input)

            logger.debug(
                "Knowledge search query: %s",
                search_query,
            )

            documents = self.retriever.retrieve(search_query)

            documents = self.reranker.rerank(
                search_query,
                documents,
            )

            final_context = self.rag.build_context(documents)

        answer = self.generate(
            user_input=user_input,
            context=final_context,
        )

        citations = self.citation_builder.build(documents)

        return GroundedAnswer(
            answer=answer,
            citations=citations,
            grounded=bool(documents),
            confidence=self.calculate_confidence(documents),
        )

    def generate(
        self,
        user_input: str,
        context: str,
    ) -> str:
        """
        Generate answer using enterprise context.
        """

        prompt = f"""
Context:

{context or "No enterprise context available."}


Question:

{user_input}


Instructions:

- Answer only using the provided context.
- Do not invent information.
- If the answer is unavailable, state that
  the information was not found.
"""

        return super().run(user_input=prompt)

    def calculate_confidence(
        self,
        documents: list,
    ) -> float:
        """
        Estimate response confidence.

        Current implementation:
        - More retrieved documents = higher confidence.

        Replace with evaluation model later.
        """

        if not documents:
            return 0.0

        confidence = min(
            len(documents) / 5,
            1.0,
        )

        return round(
            confidence,
            2,
        )
