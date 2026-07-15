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

    - Validate response grounding
    - Validate citations
    - Detect unsafe instructions
    - Prevent unsupported answers
    - Prepare extension point for
      Azure AI Content Safety
    """

    def __init__(self):

        super().__init__(
            name="SafetyAgent",
            prompt_file="safety.txt",
        )

        self.blocked_patterns = [
            "ignore previous instructions",
            "system prompt",
            "reveal secrets",
            "show api key",
            "password",
        ]

    def review(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:
        """
        Review generated answer.

        Returns:
            SafetyCheckResult
        """

        logger.info("SafetyAgent reviewing response")

        if not response:

            return self._fail(
                reason="Empty response",
                severity="high",
            )

        validation_checks = [
            self._validate_grounding(response),
            self._validate_citations(response),
            self._detect_prompt_injection(response),
        ]

        for result in validation_checks:

            if not result.safe:
                return result

        return SafetyCheckResult(
            safe=True,
            reason="Response passed safety validation.",
            severity="low",
        )

    def _validate_grounding(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:

        if not response.grounded:

            return self._fail(
                reason=("Response is not grounded " "in enterprise documentation."),
                severity="medium",
            )

        return self._pass()

    def _validate_citations(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:

        if not response.citations:

            return self._fail(
                reason=("Response does not contain " "document citations."),
                severity="medium",
            )

        return self._pass()

    def _detect_prompt_injection(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:

        answer = response.answer.lower()

        for pattern in self.blocked_patterns:

            if pattern in answer:

                return self._fail(
                    reason=("Potential prompt injection " "or sensitive disclosure detected."),
                    severity="high",
                )

        return self._pass()

    def _pass(self) -> SafetyCheckResult:

        return SafetyCheckResult(
            safe=True,
            reason="Validation passed.",
            severity="low",
        )

    def _fail(
        self,
        reason: str,
        severity: str,
    ) -> SafetyCheckResult:

        return SafetyCheckResult(
            safe=False,
            reason=reason,
            severity=severity,
        )
