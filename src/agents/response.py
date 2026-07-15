"""
Response Agent.

Constructs the final user-facing response after
planning, knowledge retrieval, and safety validation.
"""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import (
    GroundedAnswer,
    PlannerDecision,
    SafetyCheckResult,
)

logger = get_logger(__name__)


class ResponseAgent(BaseAgent):
    """
    Generates the final assistant response.

    Responsibilities:
        - Construct the final response.
        - Respect safety validation.
        - Preserve citations and confidence.
        - Provide a single extension point for future
          formatting and personalization.
    """

    def __init__(self):
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
        Generate the final response.

        Args:
            planner_decision:
                Output from PlannerAgent.

            knowledge_response:
                Grounded answer from KnowledgeAgent.

            safety_result:
                Result from SafetyAgent.

        Returns:
            Final GroundedAnswer if the response is safe,
            otherwise None.
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

        logger.info(
            "ResponseAgent completed | retrieval=%s | confidence=%.2f",
            planner_decision.requires_retrieval if planner_decision else False,
            knowledge_response.confidence,
        )

        #
        # Future enhancements can happen here:
        #
        # - Markdown formatting
        # - Citation formatting
        # - Tone adaptation
        # - Response summarization
        # - Localization
        #

        return knowledge_response
