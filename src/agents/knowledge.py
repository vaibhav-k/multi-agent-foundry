"""
Knowledge agent implementation.

This module implements the Retrieval-Augmented Generation (RAG) pipeline used
to answer enterprise knowledge requests. The agent retrieves relevant
documentation, constructs a grounded context, generates an answer using an
LLM, and attaches supporting citations.

Workflow:

    User Query
        │
        ▼
    Query Rewriting
        │
        ▼
    Document Retrieval
        │
        ▼
    Document Reranking
        │
        ▼
    Context Construction
        │
        ▼
    LLM Generation
        │
        ▼
    Citation Generation
        │
        ▼
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
    Retrieve enterprise knowledge and generate grounded responses.

    The knowledge agent orchestrates the complete Retrieval-Augmented
    Generation (RAG) workflow. It is responsible for retrieving relevant
    enterprise documentation, constructing retrieval context, generating
    grounded answers, and attaching citations.

    Responsibilities:
        - Rewrite user queries for improved retrieval.
        - Retrieve documents from the enterprise search index.
        - Rerank retrieved documents.
        - Build retrieval context for the language model.
        - Generate grounded responses.
        - Produce structured document citations.

    Notes:
        This agent is intentionally retrieval-focused. It does not perform
        safety validation or response presentation, which are handled by
        dedicated downstream agents.
    """

    def __init__(self):
        """
        Initialize the knowledge agent.

        Creates the shared RAG pipeline components required for query rewriting,
        retrieval, reranking, context construction, and citation generation.
        """

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
        Execute the complete Retrieval-Augmented Generation (RAG) workflow.

        If retrieval context is provided, it is used directly. Otherwise, the
        agent rewrites the user query, retrieves relevant enterprise documents,
        reranks the results, constructs a retrieval context, generates a grounded
        response, and produces supporting citations.

        Workflow:
            1. Rewrite the search query.
            2. Retrieve enterprise documents.
            3. Rerank retrieved documents.
            4. Build retrieval context.
            5. Generate a grounded answer.
            6. Attach supporting citations.
            7. Estimate response confidence.

        Args:
            user_input: User's natural language question.
            context: Optional precomputed retrieval context. When provided, document
                     retrieval is skipped.

        Returns: A ``GroundedAnswer`` containing the generated response, supporting
                 citations, grounding status, and confidence estimate.

        Notes:
            This method represents the primary entry point for the knowledge
            retrieval pipeline.
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
        Generate a grounded response using enterprise context.

        Constructs a prompt that restricts the language model to the supplied
        enterprise documentation and instructs it to avoid unsupported or
        fabricated information.

        Args:
            user_input: Original user question.
            context: Retrieved enterprise documentation formatted for prompting.

        Returns:
            Generated response grounded in the supplied enterprise context.
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
        Estimate response confidence from retrieval scores.

        Azure AI Search returns relevance scores rather than calibrated
        probabilities. This method converts the highest retrieval score into a
        normalized confidence value in the range ``0.0`` to ``1.0``.

        Args:
            documents: Ranked documents returned by the retrieval pipeline.

        Returns:
            Normalized confidence score for the generated response.

        Notes:
            The current implementation applies a simple heuristic based on the
            highest retrieval score. Future implementations may incorporate
            reranking scores, semantic similarity, citation agreement, or model
            confidence signals for more accurate estimation.
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
