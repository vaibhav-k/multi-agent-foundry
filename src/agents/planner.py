"""
Planner Agent.

Responsible for analysing user requests and deciding
the execution workflow.
"""

import json
import re

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import PlannerDecision

logger = get_logger(__name__)


class PlannerAgent(BaseAgent):
    """
    Planner agent.

    Responsibilities:

    - Understand user intent
    - Decide if retrieval is required
    - Decide if safety review is required
    - Create execution plan
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

        Returns:
            PlannerDecision containing routing information.
        """

        logger.info("PlannerAgent analyzing request")

        prompt = f"""
Analyze the user request and return ONLY valid JSON.

User request:

{user_input}

Return:

{{
    "intent": "short description",
    "requires_retrieval": true,
    "requires_safety_review": true,
    "execution_steps": [
        "step1",
        "step2"
    ]
}}
"""

        response = super().run(user_input=prompt)

        logger.debug(f"Planner output: {response}")

        return self._parse_plan(
            response,
        )

    def _parse_plan(
        self,
        response: str,
    ) -> PlannerDecision:
        """
        Convert planner LLM output into
        PlannerDecision.

        Falls back safely if the model
        returns invalid JSON.
        """

        try:

            json_text = self._extract_json(response)

            data = json.loads(json_text)

            return PlannerDecision(
                intent=data.get("intent"),
                requires_retrieval=data.get(
                    "requires_retrieval",
                    True,
                ),
                requires_safety_review=data.get(
                    "requires_safety_review",
                    True,
                ),
                execution_steps=data.get(
                    "execution_steps",
                    [],
                ),
            )

        except Exception:

            logger.warning("Planner output parsing failed. " "Using default workflow.")

            return PlannerDecision(
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
        Extract JSON object from model output.
        """

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if not match:
            raise ValueError("No JSON found in planner output")

        return match.group(0)
