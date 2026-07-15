"""
Multi-agent orchestration layer.

Coordinates:

- Planner Agent
- Knowledge Agent
- Safety Agent
- ResponseAgent

using shared AgentState.
"""

from __future__ import annotations

import time

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
    ResponseAgent,
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
        Response Agent
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
        response_agent: ResponseAgent | None = None,
    ):
        self.planner = planner
        self.knowledge_agent = knowledge_agent or KnowledgeAgent()
        self.safety_agent = safety_agent or SafetyAgent()
        self.state_manager = state_manager or StateManager()
        self.response_agent = response_agent or ResponseAgent()

        logger.info("Multi-agent orchestrator initialized")

    def run(
        self,
        user_input: str,
        conversation_id: str = "default",
    ) -> AgentWorkflowResult:

        workflow_start = time.perf_counter()

        logger.info(f"Starting workflow | conversation_id={conversation_id}")

        state = self.state_manager.create(
            conversation_id=conversation_id,
            message=user_input,
        )

        self._run_planner(
            state,
            user_input,
        )

        self._run_knowledge(
            state,
            user_input,
        )

        self._run_safety(
            state,
        )

        self._run_response(
            state,
        )

        logger.info(
            f"Workflow completed | duration={time.perf_counter() - workflow_start:.2f}s"
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

        logger.info(f"Planner completed | duration={time.perf_counter() - start:.2f}s")

    def _run_knowledge(
        self,
        state: AgentState,
        user_input: str,
    ) -> None:
        """
        Execute KnowledgeAgent only when required.
        """

        plan = state.planner_decision

        if not plan:
            logger.warning("Knowledge skipped | no planner decision")
            return

        if not plan.requires_retrieval:

            logger.info("Knowledge skipped | retrieval not required")

            return

        start = time.perf_counter()

        state.knowledge_response = self.knowledge_agent.answer(
            user_input=user_input,
        )

        logger.info(f"Knowledge completed | duration={time.perf_counter() - start:.2f}s")


    def _run_safety(
        self,
        state: AgentState,
    ) -> None:
        """
        Execute SafetyAgent based on planner decision.
        """

        plan = state.planner_decision

        if not plan:
            return

        if not plan.requires_safety_review:

            logger.info("Safety skipped | not required")

            state.safety_passed = True

            return

        if not state.knowledge_response:

            logger.warning("Safety skipped | no response available")

            return

        start = time.perf_counter()

        state.safety_result = self.safety_agent.review(state.knowledge_response)

        state.safety_passed = state.safety_result.safe

        logger.info(
            f"Safety completed | passed={state.safety_passed} | duration={time.perf_counter() - start:.2f}s"
        )

    def _run_response(
        self,
        state: AgentState,
    ) -> None:
        """
        Execute ResponseAgent.
        """

        start = time.perf_counter()

        state.final_answer = self.response_agent.generate(
            state.planner_decision,
            state.knowledge_response,
            state.safety_result,
        )

        if state.final_answer:
            state.response = state.final_answer.answer
        else:
            state.response = (
                "The request could not be completed because it did not pass safety validation."
            )

        logger.info(f"Response completed | duration={time.perf_counter() - start:.2f}s")

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
