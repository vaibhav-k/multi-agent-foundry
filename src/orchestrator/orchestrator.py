"""
Multi-agent orchestration layer.

Coordinates:

- Planner Agent
- Knowledge Agent
- Safety Agent

using shared AgentState.
"""

from __future__ import annotations

import time

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
)
from src.config import get_logger
from src.models import AgentWorkflowResult
from src.orchestrator.state import StateManager
from src.state.models import AgentState

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
        Execute complete agent workflow.
        """

        workflow_start = time.perf_counter()

        logger.info(
            "Starting workflow | conversation_id=%s",
            conversation_id,
        )

        state = self.state_manager.create(
            conversation_id=conversation_id,
            message=user_input,
        )

        self._run_planner(state, user_input)

        self._run_knowledge(
            state,
            user_input,
        )

        self._run_safety(state)

        self._build_response(state)

        elapsed = time.perf_counter() - workflow_start

        logger.info(
            "Workflow completed | duration=%.2fs",
            elapsed,
        )

        return self.to_workflow_result(state)

    def _run_planner(
        self,
        state: AgentState,
        user_input: str,
    ) -> None:
        """
        Execute planner agent.
        """

        start = time.perf_counter()

        state.planner_decision = self.planner.plan(user_input)

        logger.info(
            "Planner completed | duration=%.2fs",
            time.perf_counter() - start,
        )

    def _run_knowledge(
        self,
        state: AgentState,
        user_input: str,
    ) -> None:
        """
        Execute knowledge retrieval and generation.
        """

        if not state.planner_decision:
            return

        if not state.planner_decision.requires_retrieval:
            logger.info("Knowledge skipped | retrieval not required")
            return

        start = time.perf_counter()

        state.knowledge_response = self.knowledge_agent.answer(
            user_input=user_input,
        )

        logger.info(
            "Knowledge completed | duration=%.2fs",
            time.perf_counter() - start,
        )

    def _run_safety(
        self,
        state: AgentState,
    ) -> None:
        """
        Execute safety review.
        """

        if not state.knowledge_response:
            return

        start = time.perf_counter()

        state.safety_result = self.safety_agent.review(state.knowledge_response)

        state.safety_passed = state.safety_result.safe

        logger.info(
            "Safety completed | passed=%s | duration=%.2fs",
            state.safety_passed,
            time.perf_counter() - start,
        )

    def _build_response(
        self,
        state: AgentState,
    ) -> None:
        """
        Construct final workflow response.
        """

        if state.safety_passed:
            state.final_answer = state.knowledge_response

            state.response = state.knowledge_response.answer

            return

        state.response = (
            "The request could not be completed "
            "because it did not pass safety validation."
        )

    def to_workflow_result(
        self,
        state: AgentState,
    ) -> AgentWorkflowResult:
        """
        Convert runtime state into API response model.
        """

        return AgentWorkflowResult(
            user_query=state.user_message,
            planner_output=state.planner_decision,
            knowledge_output=state.knowledge_response,
            safety_output=state.safety_result,
            final_response=state.final_answer,
            success=(state.safety_passed or state.final_answer is not None),
            metadata=state.metadata,
        )
