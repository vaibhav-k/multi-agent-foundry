"""
Safety agent implementation.

This module defines the safety validation stage of the multi-agent workflow.
The safety agent evaluates grounded responses before they are returned to the
user, ensuring they satisfy enterprise safety and compliance requirements.

The current implementation performs lightweight rule-based validation and is
designed to be extended with Azure AI Content Safety and additional policy
engines.

Workflow:

    Grounded Response
            │
            ▼
    Grounding Validation
            │
            ▼
    Citation Validation
            │
            ▼
    Prompt Injection Detection
            │
            ▼
    Safety Decision
"""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.config import get_logger
from src.models import (
    GroundedAnswer,
    SafetyCheckResult,
)

logger = get_logger(__name__)


class SafetyAgent(BaseAgent):
    """
    Validate generated responses against enterprise safety policies.

    The safety agent performs rule-based validation on grounded responses
    before they are returned to the user. Its primary objective is to prevent
    unsupported, unsafe, or policy-violating content from leaving the
    application.

    Current responsibilities:
        - Verify that responses are grounded.
        - Ensure supporting citations are present.
        - Detect basic prompt injection attempts.
        - Detect requests for sensitive information.
        - Produce a structured safety decision.

    Notes:
        This implementation intentionally performs lightweight validation.
        It serves as an extension point for enterprise-grade content safety
        services and custom policy engines.

    Future enhancements:
        - Azure AI Content Safety integration.
        - Toxicity and harmful content detection.
        - Personally identifiable information (PII) detection.
        - Secret and credential leakage detection.
        - Hallucination detection using citation verification.
        - Compliance policy validation.
        - Risk scoring instead of binary pass/fail decisions.
        - Audit logging and policy explanations.
        - Configurable organization-specific safety rules.
    """

    def __init__(self):
        """
        Initialize the safety agent.

        Loads the safety validation prompt and configures the built-in
        rule-based validation patterns.
        """
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
        Validate a grounded response.

        The response is evaluated using a sequence of validation rules. The
        first failed validation immediately terminates the review and returns
        a failure result.

        Validation steps:
            1. Verify grounding.
            2. Verify supporting citations.
            3. Detect prompt injection or sensitive disclosures.

        Args:
            response: Grounded response produced by the knowledge agent.

        Returns:
            A ``SafetyCheckResult`` indicating whether the response satisfies
            enterprise safety requirements.
        """

        logger.info("SafetyAgent reviewing response")

        if response is None:
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
                logger.warning(
                    "Safety validation failed: %s",
                    result.reason,
                )
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
        """
        Verify that the response is grounded in enterprise documentation.

        Args:
            response: Generated grounded response.

        Returns:
            Validation result.
        """

        if not response.grounded:
            return self._fail(
                reason=("Response is not grounded in enterprise documentation."),
                severity="medium",
            )

        return self._pass()

    def _validate_citations(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:
        """
        Verify that the response contains supporting citations.

        Args:
            response: Generated grounded response.

        Returns:
            Validation result.
        """

        if not response.citations:
            return self._fail(
                reason="Response does not include supporting citations.",
                severity="medium",
            )

        return self._pass()

    def _detect_prompt_injection(
        self,
        response: GroundedAnswer,
    ) -> SafetyCheckResult:
        """
        Detect simple prompt injection and sensitive disclosure attempts.

        The current implementation performs keyword matching against known
        prompt injection patterns. This provides lightweight protection and
        should be supplemented by dedicated content safety services in
        production deployments.

        Args:
            response: Generated grounded response.

        Returns:
            Validation result.
        """

        answer = response.answer.lower()

        for pattern in self.blocked_patterns:
            if pattern in answer:
                return self._fail(
                    reason=(
                        "Potential prompt injection or sensitive information "
                        "disclosure detected."
                    ),
                    severity="high",
                )

        return self._pass()

    def _pass(self) -> SafetyCheckResult:
        """
        Create a successful validation result.

        Returns:
            Successful safety validation result.
        """

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
        """
        Create a failed validation result.

        Args:
            reason: Human-readable explanation of the validation failure.
            severity: Severity level associated with the failure.

        Returns:
            Failed safety validation result.
        """

        return SafetyCheckResult(
            safe=False,
            reason=reason,
            severity=severity,
        )
