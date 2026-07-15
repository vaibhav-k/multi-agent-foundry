"""
Response agent implementation.

This module defines the final stage of the agent pipeline. The response agent
combines outputs from planning, retrieval, and safety validation to produce
the final user-facing response.

Unlike retrieval or planning agents, the response agent focuses on
presentation rather than reasoning. It is responsible for formatting,
metadata enrichment, and output preparation.
"""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import (
    DocumentReference,
    GroundedAnswer,
    PlannerDecision,
    SafetyCheckResult,
)

logger = get_logger(__name__)


class ResponseAgent(BaseAgent):
    """
    Assemble the final response returned to the user.

    Responsibilities:
        - Validate safety approval.
        - Format the generated answer.
        - Normalize citations.
        - Deduplicate sources.
        - Add confidence metadata.
        - Provide a single extension point for presentation logic.

    This class intentionally avoids modifying factual content. Any reasoning,
    retrieval, summarization, or personalization should be performed by
    upstream agents.
    """

    def __init__(self):
        """Initialize the response agent."""
        super().__init__(
            name="ResponseAgent",
            prompt_file="rag_answer.txt",
        )

    def generate(
        self,
        planner_decision: PlannerDecision | None,
        knowledge_response: GroundedAnswer | None,
        safety_result: SafetyCheckResult | None,
    ) -> GroundedAnswer | None:
        """
        Produce the final user-facing response.

        Args:
            planner_decision:
                Output from the planner agent.

            knowledge_response:
                Grounded answer returned by the knowledge agent.

            safety_result:
                Output from the safety validation stage.

        Returns:
            A formatted ``GroundedAnswer`` if the response is approved,
            otherwise ``None``.
        """

        if knowledge_response is None:
            logger.warning("No knowledge response available.")
            return None

        if safety_result is not None and not safety_result.safe:
            logger.warning(
                "Response blocked by safety validation: %s",
                safety_result.reason,
            )
            return None

        #
        # -----------------------------
        # Presentation enhancements
        # -----------------------------
        #

        knowledge_response.citations = self._deduplicate_citations(knowledge_response.citations)

        logger.info(
            "ResponseAgent completed | retrieval=%s | confidence=%.2f | sources=%d",
            planner_decision.requires_retrieval if planner_decision else False,
            knowledge_response.confidence,
            len(knowledge_response.citations),
        )

        return knowledge_response

    # ------------------------------------------------------------------ #
    # Presentation helpers
    # ------------------------------------------------------------------ #

    def _deduplicate_sources(
        self,
        sources: list[str],
    ) -> list[str]:
        """
        Remove duplicate citations while preserving order.
        """
        return list(dict.fromkeys([i.name for i in sources]))

    def _deduplicate_citations(
        self,
        citations: list[DocumentReference],
    ) -> list[DocumentReference]:
        """Remove duplicate citation references."""

        seen = set()
        unique = []

        for citation in citations:
            key = (
                citation.document_id,
                citation.name,
                citation.section,
            )

            if key not in seen:
                seen.add(key)
                unique.append(citation)

        return unique

    def _append_sources(
        self,
        text: str,
        sources: list[str],
    ) -> str:
        """
        Append a formatted references section.

        Future enhancements:
            - APA/MLA formatting
            - Hyperlinks
            - Citation numbering
            - DOI resolution
        """

        if not sources:
            return text

        references = "\n".join(f"- {source}" for source in sources)

        return f"{text}\n\n### Sources\n{references}"
