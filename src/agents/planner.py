"""
Planner Agent.

Responsible for analysing user requests and deciding
the execution workflow.
"""

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
    Analyze the user request.

    User request:
    {user_input}

    Decide:

    1. Does this require enterprise document retrieval?
    2. Does the response require safety validation?
    3. What execution steps are needed?
    """

        response = super().run(user_input=prompt)

        # Temporary deterministic routing.
        # Replace with structured LLM output later.

        return PlannerDecision(
            requires_retrieval=True,
            requires_safety_review=True,
            execution_steps=[
                "retrieve_documents",
                "generate_grounded_answer",
                "validate_safety",
            ],
        )
