"""
Planner agent implementation.

This module defines the planning stage of the multi-agent workflow. The
planner analyzes a user's request and produces a structured execution plan
that the orchestrator uses to coordinate downstream agents.

The planner is responsible for understanding user intent rather than
retrieving knowledge or generating responses.

Workflow:

    User Request
         │
         ▼
    Intent Analysis
         │
         ▼
    Execution Planning
         │
         ▼
    PlannerDecision
         │
         ▼
    Orchestrator
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
    Analyze user requests and determine the execution workflow.

    The planner serves as the entry point to the multi-agent pipeline. It
    interprets the user's request and produces a structured
    :class:`PlannerDecision` that instructs the orchestrator how to process
    the request.

    Responsibilities:
        - Identify the user's intent.
        - Determine whether enterprise retrieval is required.
        - Determine whether safety validation should be performed.
        - Produce an ordered execution plan for downstream agents.

    Notes:
        The current implementation always enables document retrieval and
        safety validation to ensure responses remain grounded in enterprise
        knowledge and comply with application policies.

    Future enhancements:
        - Intent classification using dedicated models.
        - Dynamic workflow selection.
        - Tool and function routing.
        - Multi-step task decomposition.
        - Parallel execution planning.
        - Confidence-aware routing.
        - Cost and latency optimization.
        - Conversation-aware planning.
    """

    def __init__(self):
        """
        Initialize the planner agent.

        Loads the planning prompt and initializes the shared Azure AI
        Foundry client through the base agent.
        """
        super().__init__(
            name="PlannerAgent",
            prompt_file="planner.txt",
        )

    def plan(
        self,
        user_input: str,
    ) -> PlannerDecision:
        """
        Generate an execution plan for a user request.

        The planner invokes the language model to analyze the user's request,
        parses the structured planning response, and returns a validated
        ``PlannerDecision``.

        Args:
            user_input:
                User request to analyze.

        Returns:
            A validated ``PlannerDecision`` describing the execution workflow.

        Notes:
            If the language model returns an invalid or malformed response,
            the planner automatically falls back to a predefined safe
            execution plan.
        """

        logger.info("PlannerAgent analyzing request")

        response = super().run(user_input=user_input)

        logger.debug("Planner output: %s", response)

        return self._parse_plan(response)

    def _parse_plan(
        self,
        response: str,
    ) -> PlannerDecision:
        """
        Parse the language model response into a planner decision.

        The planner expects a JSON object containing workflow metadata.
        Invalid or incomplete responses automatically fall back to the
        default execution plan.

        Args:
            response:
                Raw language model response.

        Returns:
            Parsed ``PlannerDecision``.
        """

        try:
            json_text = self._extract_json(response)

            data = json.loads(json_text)

            return PlannerDecision(
                intent=data.get(
                    "intent",
                    "enterprise knowledge request",
                ),
                requires_retrieval=True,
                requires_safety_review=True,
                execution_steps=[
                    "retrieve_documents",
                    "generate_grounded_answer",
                    "validate_safety",
                    "generate_response",
                ],
            )

        except Exception:
            logger.warning(
                "Planner response could not be parsed. "
                "Falling back to the default execution plan."
            )

            return DEFAULT_PLAN

    def _extract_json(
        self,
        text: str,
    ) -> str:
        """
        Extract a JSON object from a language model response.

        The planner accepts both plain JSON responses and Markdown code
        blocks containing JSON.

        Supported formats:

        Plain JSON::

            {
                "intent": "vpn setup"
            }

        Markdown::

            ```json
            {
                "intent": "vpn setup"
            }
            ```

        Args:
            text:
                Raw language model output.

        Returns:
            Extracted JSON string.

        Raises:
            ValueError:
                If no JSON object can be located in the response.
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
            raise ValueError("No JSON object found in planner response.")

        return json_match.group(0)
