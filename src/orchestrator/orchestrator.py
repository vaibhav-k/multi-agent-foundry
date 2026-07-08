"""
Multi-agent orchestration layer.

Coordinates:
- Planner Agent
- Knowledge Agent
- Safety Agent
"""

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
)

from src.config import get_logger

from src.models import AgentWorkflowResult

logger = get_logger(__name__)


class Orchestrator:
    """
    Coordinates the complete agent workflow.

    Workflow:

        User Request
              |
              v
        Planner Agent
              |
              v
        Knowledge Agent
              |
              v
        Safety Agent
              |
              v
        Final Response
    """

    def __init__(
        self,
        planner: PlannerAgent,
        knowledge_agent: KnowledgeAgent,
        safety_agent: SafetyAgent,
    ):
        self.planner = planner
        self.knowledge_agent = knowledge_agent
        self.safety_agent = safety_agent

        logger.info("Multi-agent orchestrator initialized")

    def run(
        self,
        user_input: str,
    ) -> AgentWorkflowResult:
        """
        Execute agent workflow.
        """

        logger.info("Starting workflow")

        # -------------------------------------------------
        # Step 1: Planning
        # -------------------------------------------------

        planner_output = self.planner.plan(user_input)

        logger.info("Planner completed")

        # -------------------------------------------------
        # Step 2: Knowledge Retrieval / Answer Generation
        # -------------------------------------------------

        knowledge_output = self.knowledge_agent.answer(
            user_input=user_input,
        )

        logger.info("Knowledge agent completed")

        # -------------------------------------------------
        # Step 3: Safety Review
        # -------------------------------------------------

        safety_output = self.safety_agent.review(knowledge_output)

        logger.info("Safety review completed")

        # -------------------------------------------------
        # Step 4: Final response
        # -------------------------------------------------

        return AgentWorkflowResult(
            user_query=user_input,
            planner_output=planner_output,
            knowledge_output=knowledge_output,
            safety_output=safety_output,
            final_response=knowledge_output,
            success=True,
        )
