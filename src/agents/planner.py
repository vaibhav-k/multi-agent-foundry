"""
Planner Agent.

Responsible for analysing user requests and deciding
the execution workflow.
"""

from src.agents.base import BaseAgent
from src.config import get_logger

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
    ) -> str:
        """
        Generate execution plan.

        Uses the BaseAgent model invocation.
        """

        logger.info("Creating plan for request")

        return super().run(user_input=user_input)
