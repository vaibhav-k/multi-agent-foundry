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

from typing import List, Optional

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import GroundedAnswer

from src.rag import (
    RAGBuilder,
    RAGRetriever,
)

from src.rag.citations import CitationBuilder
from src.rag.models import RAGDocument
from src.rag.reranker import DocumentReranker
from src.rag.query import QueryRewriter

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

        documents: List[RAGDocument] = []

        if context:

            logger.debug("Using provided context")

            final_context = context

        else:

            search_query = self.query_rewriter.rewrite(user_input)

            logger.debug(f"Rewritten search query: {search_query}")

            documents = self.retriever.retrieve(search_query)

            logger.info(f"Retrieved {len(documents)} documents")

            documents = self.reranker.rerank(query=search_query, documents=documents)

            logger.info(f"Reranked documents: {len(documents)}")

            final_context = self.rag.build_context(documents)

            logger.debug(f"Generated RAG context:\n{final_context}")

        answer = self.generate(
            user_input,
            final_context,
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
        Generate a grounded response.
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
        documents: list[RAGDocument],
    ) -> float:
        """
        Calculate normalized confidence from retrieval scores.

        Azure AI Search scores are relevance scores,
        not probabilities. Normalize them into
        a 0-1 confidence range.
        """

        if not documents:
            return 0.0

        scores = []

        for document in documents:

            if document.score is not None:
                scores.append(float(document.score))

        if not scores:
            return 0.0

        highest_score = max(scores)

        confidence = min(
            highest_score / 5.0,
            1.0,
        )

        return round(
            confidence,
            2,
        )
