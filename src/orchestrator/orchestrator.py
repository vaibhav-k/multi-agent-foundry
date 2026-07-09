"""
Multi-agent orchestration layer.

Coordinates:

- Planner Agent
- Knowledge Agent
- Safety Agent

using shared AgentState.
"""

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
)

from src.config import get_logger

from src.models import AgentWorkflowResult

from src.state.models import AgentState

from src.orchestrator.state import StateManager

logger = get_logger(__name__)


class Orchestrator:
    """
    Coordinates the complete agent workflow.

    Workflow:

        User Request
              |
              v
          AgentState
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
        knowledge_agent: KnowledgeAgent | None = None,
        safety_agent: SafetyAgent | None = None,
        state_manager: StateManager | None = None,
    ):

        self.planner = planner

        self.knowledge_agent = knowledge_agent if knowledge_agent else KnowledgeAgent()

        self.safety_agent = safety_agent if safety_agent else SafetyAgent()

        self.state_manager = state_manager if state_manager else StateManager()

        logger.info("Multi-agent orchestrator initialized")

    def run(
        self,
        user_input: str,
        conversation_id: str = "default",
    ) -> AgentWorkflowResult:
        """
        Execute agent workflow.

        Creates AgentState and passes it
        through the agent lifecycle.
        """

        logger.info("Starting workflow")

        state = self.state_manager.create(
            conversation_id=conversation_id,
            message=user_input,
        )

        # -------------------------------------------------
        # Step 1: Planner Agent
        # -------------------------------------------------

        state.planner_decision = self.planner.plan(user_input)

        logger.info("Planner completed")

        # -------------------------------------------------
        # Step 2: Knowledge Agent
        # -------------------------------------------------

        if state.planner_decision and state.planner_decision.requires_retrieval:

            state.knowledge_response = self.knowledge_agent.answer(
                user_input=user_input,
            )

            logger.info("Knowledge agent completed")

        # -------------------------------------------------
        # Step 3: Safety Agent
        # -------------------------------------------------

        if state.knowledge_response:

            state.safety_result = self.safety_agent.review(state.knowledge_response)

            state.safety_passed = state.safety_result.safe

            logger.info("Safety review completed")

        # -------------------------------------------------
        # Step 4: Final Response
        # -------------------------------------------------

        if state.safety_passed:

            state.final_answer = state.knowledge_response

            state.response = state.knowledge_response.answer

        else:

            state.response = (
                "The request could not be completed "
                "because it did not pass safety validation."
            )

        logger.info("Workflow completed")

        return self.to_workflow_result(state)

    def to_workflow_result(
        self,
        state: AgentState,
    ) -> AgentWorkflowResult:
        """
        Convert runtime state into API response model.
        """

        return AgentWorkflowResult(
            user_query=state.user_message,
            planner_output=(state.planner_decision),
            knowledge_output=(state.knowledge_response),
            safety_output=(state.safety_result),
            final_response=(state.final_answer),
            success=(state.safety_passed or state.final_answer is not None),
            metadata=state.metadata,
        )
