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

from typing import Optional, List, Dict

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import GroundedAnswer

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

    - Rewrite user queries
    - Retrieve enterprise documents
    - Rerank search results
    - Build grounded context
    - Generate answers
    - Provide citations
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
        Execute complete RAG workflow.

        Flow:

        1. Rewrite query
        2. Retrieve documents
        3. Rerank documents
        4. Build context
        5. Generate grounded answer
        6. Attach citations
        """

        logger.info("KnowledgeAgent processing request")

        documents: List[Dict] = []

        if context:

            logger.debug("Using provided context")

            final_context = context

        else:

            search_query = self.query_rewriter.rewrite(user_input)

            logger.debug(f"Rewritten search query: {search_query}")

            retrieved_documents = self.retriever.retrieve(search_query)

            logger.info(f"Retrieved {len(retrieved_documents)} documents")

            # documents = self.reranker.rerank(
            #     search_query,
            #     retrieved_documents,
            # )
            documents = retrieved_documents

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
            confidence=(self.calculate_confidence(documents)),
        )

    def generate(
        self,
        user_input: str,
        context: str,
    ) -> str:
        """
        Generate grounded response.
        """

        prompt = f"""
You are an enterprise IT knowledge assistant.

Rules:

- Answer only using approved enterprise documentation.
- Do not use external knowledge.
- Do not guess or fabricate information.
- If information is unavailable, respond:

"The information was not found in approved documentation."


Enterprise Context:

{context or "No enterprise documentation found."}


User Question:

{user_input}


Answer:
"""

        return super().run(user_input=prompt)

    def calculate_confidence(
        self,
        documents: list,
    ) -> float:
        """
        Calculate normalized confidence score.

        Uses:
        - retrieval availability
        - reranker/search score

        Returns:
            Float between 0 and 1.
        """

        if not documents:
            return 0.0

        scores = []

        for document in documents:

            score = document.get(
                "score",
                0,
            )

            scores.append(score)

        if not scores:
            return 0.0

        average_score = sum(scores) / len(scores)

        # Normalize Azure Search score
        confidence = min(
            average_score / 5,
            1.0,
        )

        return round(
            confidence,
            2,
        )
