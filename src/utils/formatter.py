"""
Response formatting utilities.

Provides human-readable representations of
agent workflow results.
"""

from __future__ import annotations

from src.models import AgentWorkflowResult


def format_workflow_result(
    result: AgentWorkflowResult,
) -> str:
    """
    Convert workflow result into human-readable CLI output.

    Args:
        result: Completed multi-agent workflow result.

    Returns:
        Formatted response string.
    """

    if not result.final_response:
        return _format_empty_response()

    response = result.final_response

    return "\n".join(
        [
            _section_header("RESPONSE"),
            "",
            response.answer,
            "",
            _format_sources(response.citations),
            "",
            _format_confidence(response.confidence),
            "",
            _format_safety(result.success),
        ]
    )


def _section_header(title: str) -> str:
    """
    Format a CLI section header.
    """
    return f"========== {title} =========="


def _format_sources(citations: list | None) -> str:
    """
    Format response citations.
    """

    if not citations:
        return "Sources\n" "-------\n" "- No sources found"

    sources = "\n".join(f"- {citation.name}" for citation in citations)

    return "Sources\n" "-------\n" f"{sources}"


def _format_confidence(
    confidence: float | None,
) -> str:
    """
    Format confidence score.
    """

    if confidence is None:
        return "Confidence\n" "----------\n" "Unknown"

    percentage = int(confidence * 100)

    return "Confidence\n" "----------\n" f"{percentage}%"


def _format_safety(success: bool) -> str:
    """
    Format safety result.
    """

    status = "✓ PASSED" if success else "✗ FAILED"

    return "Safety\n" "------\n" f"{status}"


def _format_empty_response() -> str:
    """
    Format missing response output.
    """

    return "\n".join(
        [
            _section_header("RESPONSE"),
            "",
            "No response generated.",
        ]
    )
