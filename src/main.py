"""
Enterprise IT Knowledge Assistant.

Application entry point.
"""

from src.bootstrap import create_orchestrator
from src.config import configure_logging, get_logger
from src.utils.formatter import format_workflow_result

configure_logging()

logger = get_logger(__name__)


def main() -> None:
    """Run the Enterprise IT Knowledge Assistant."""

    logger.info("Starting Enterprise IT Knowledge Assistant")

    orchestrator = create_orchestrator()

    user_request = "How do I connect to the company VPN?"

    result = orchestrator.run(user_request)

    print(format_workflow_result(result))


if __name__ == "__main__":
    main()
