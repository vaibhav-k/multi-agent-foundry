"""
Enterprise IT Knowledge Assistant.

Application entry point.
"""

from __future__ import annotations

import uuid

from src.bootstrap import create_orchestrator
from src.config import configure_logging, get_logger
from src.utils.formatter import format_workflow_result

configure_logging()

logger = get_logger(__name__)

TEST_QUESTIONS = [
    "How do I enroll in MFA?",
    "What does mobile access require?",
    "How do I connect to the company VPN?",
    "What are the password requirements?",
    "How do I configure Outlook?",
    "How do I install approved software?",
    "How do I report a security incident?",
]


def main() -> None:
    """
    Run the Enterprise IT Knowledge Assistant against
    a set of representative test questions.
    """

    logger.info("Starting Enterprise IT Knowledge Assistant")

    orchestrator = create_orchestrator()

    # Use one conversation to exercise conversation memory.
    conversation_id = str(uuid.uuid4())

    for index, question in enumerate(TEST_QUESTIONS, start=1):

        logger.info(f"Running test question {index}/{len(TEST_QUESTIONS)}")

        print("\n" + "=" * 80)
        print(f"QUESTION {index}: {question}")
        print("=" * 80)

        try:
            result = orchestrator.run(
                user_input=question,
                conversation_id=conversation_id,
            )

            print(format_workflow_result(result))

        except Exception:
            logger.exception(f"Failed processing question: {question}")

            print("ERROR: Request failed.\n")


if __name__ == "__main__":
    main()
