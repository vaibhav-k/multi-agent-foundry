"""
Planner Agent.

Responsible for analysing user requests and deciding
the execution workflow.

The planner produces a structured PlannerDecision
used by the orchestrator for routing.
"""

from __future__ import annotations

import json
import re

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import PlannerDecision

logger = get_logger(__name__)


DEFAULT_PLAN = PlannerDecision(
    requires_retrieval=True,
    requires_safety_review=True,
    execution_steps=[
        "retrieve_documents",
        "generate_grounded_answer",
        "validate_safety",
        "generate_response",
    ],
)


class PlannerAgent(BaseAgent):
    """
    Determines workflow execution strategy.

    Responsibilities:

    - Understand user intent
    - Decide retrieval requirement
    - Decide safety requirement
    - Produce execution steps
    """

    def __init__(self):

        super().__init__(
            name="PlannerAgent",
            prompt_file="planner.txt",
        )

    def plan(
        self,
        user_input: str,
    ) -> PlannerDecision:
        """
        Decide workflow execution.
        """

        logger.info("PlannerAgent analyzing request")

        response = super().run(user_input=user_input)

        logger.debug(f"Planner output: {response}")

        return self._parse_plan(response)

    def _parse_plan(
        self,
        response: str,
    ) -> PlannerDecision:

        try:
            json_text = self._extract_json(response)

            data = json.loads(json_text)

            return PlannerDecision(
                intent=data.get(
                    "intent",
                    "enterprise knowledge request",
                ),
                # Knowledge assistant always grounds answers
                requires_retrieval=True,
                # Safety always runs
                requires_safety_review=True,
                execution_steps=[
                    "retrieve_documents",
                    "generate_grounded_answer",
                    "validate_safety",
                    "generate_response",
                ],
            )

        except Exception:

            logger.warning("Planner parsing failed. " "Using safe default workflow.")

            return PlannerDecision(
                intent="enterprise knowledge request",
                requires_retrieval=True,
                requires_safety_review=True,
                execution_steps=[
                    "retrieve_documents",
                    "generate_grounded_answer",
                    "validate_safety",
                    "generate_response",
                ],
            )

    def _extract_json(
        self,
        text: str,
    ) -> str:
        """
        Extract JSON from plain text or markdown output.
        """

        fenced_match = re.search(
            r"```json\s*(.*?)```",
            text,
            re.DOTALL,
        )

        if fenced_match:

            return fenced_match.group(1).strip()

        json_match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if not json_match:

            raise ValueError("No JSON object found")

        return json_match.group(0)
