"""
Safety Agent.

Validates generated responses against
enterprise safety policies.
"""

from src.agents.base import BaseAgent

from src.config import get_logger

from src.models import (
    GroundedAnswer,
    SafetyCheckResult,
)

logger = get_logger(__name__)


class SafetyAgent(BaseAgent):
    """
    Enterprise response safety validator.

    Responsibilities:

    - Detect unsafe responses
    - Validate grounding
    - Prevent unauthorized disclosure
    - Enforce policy rules
    """

    def __init__(self):

        super().__init__(
            name="SafetyAgent",
            prompt_file="safety.txt",
        )

    def review(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:
        """
        Review generated answer.

        Args:
            response:
                Grounded knowledge response.

        Returns:
            SafetyCheckResult
        """

        logger.info("SafetyAgent reviewing response")

        if not response:

            return SafetyCheckResult(
                safe=False,
                reason="Empty response",
                severity="high",
            )

        # ---------------------------------------------
        # Basic grounding validation
        # ---------------------------------------------

        if not response.grounded:

            return SafetyCheckResult(
                safe=False,
                reason=("Response is not grounded " "in enterprise documentation."),
                severity="medium",
            )

        # ---------------------------------------------
        # Future:
        # Azure AI Content Safety evaluation
        # Prompt injection checks
        # PII detection
        # ---------------------------------------------

        return SafetyCheckResult(
            safe=True,
            reason=("Response passed safety validation."),
            severity="low",
        )
