"""
Agent orchestration layer.

Responsible for routing user requests
through the appropriate agents.
"""

from typing import Any

from src.config import get_logger

logger = get_logger(__name__)


class Orchestrator:
    """
    Coordinates multi-agent execution.

    Current workflow:

        User Request
              |
              v
        Planner Agent
              |
              v
        Future:
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
        planner: Any,
        knowledge_agent: Any = None,
        safety_agent: Any = None,
    ):
        """
        Initialize orchestrator.

        Args:
            planner:
                Planner agent responsible for deciding workflow.

            knowledge_agent:
                Agent responsible for RAG retrieval.

            safety_agent:
                Agent responsible for response validation.
        """

        self.planner = planner
        self.knowledge_agent = knowledge_agent
        self.safety_agent = safety_agent

        logger.info("Orchestrator initialized")

    def run(
        self,
        user_input: str,
    ):
        """
        Execute agent workflow.

        Phase 1:
            Route request to planner.

        Future phases:
            1. Planner determines intent
            2. Knowledge agent retrieves context
            3. Safety agent validates response
            4. Final answer returned
        """

        logger.info(
            "Processing request: %s",
            user_input,
        )

        planner_response = self.planner.run(user_input)

        return planner_response
