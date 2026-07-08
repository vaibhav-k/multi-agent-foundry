"""
Enterprise IT Knowledge Assistant.

Application entry point.

Initializes:
- Planner Agent
- Knowledge Agent
- Safety Agent
- Orchestrator

and executes the multi-agent workflow.
"""

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
)

from src.config import get_logger

from src.orchestrator import Orchestrator

logger = get_logger(__name__)


def main():
    """
    Start the multi-agent application.
    """

    logger.info("Starting Enterprise IT Knowledge Assistant")

    # -------------------------------------------------
    # Initialize agents
    # -------------------------------------------------

    planner_agent = PlannerAgent()

    knowledge_agent = KnowledgeAgent()

    safety_agent = SafetyAgent()

    # -------------------------------------------------
    # Initialize orchestrator
    # -------------------------------------------------

    orchestrator = Orchestrator(
        planner=planner_agent,
        knowledge_agent=knowledge_agent,
        safety_agent=safety_agent,
    )

    # -------------------------------------------------
    # User request
    # -------------------------------------------------

    user_request = "How do I connect to the company VPN?"

    # -------------------------------------------------
    # Execute workflow
    # -------------------------------------------------

    result = orchestrator.run(user_request)

    # -------------------------------------------------
    # Display result
    # -------------------------------------------------

    print("\n========== WORKFLOW RESULT ==========\n")

    print("User Request:")

    print(result.user_query)

    print("\nPlanner Output:")

    print(result.planner_output)

    print("\nKnowledge Response:")

    print(result.knowledge_output)

    print("\nSafety Review:")

    print(result.safety_output)

    print("\nFinal Response:")

    print(result.final_response)

    print(
        "\nSuccess:",
        result.success,
    )


if __name__ == "__main__":

    main()
