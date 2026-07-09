"""
Response formatting utilities.
"""

from src.models import AgentWorkflowResult


def format_workflow_result(
    result: AgentWorkflowResult,
) -> str:
    """
    Convert workflow result into
    human-readable CLI output.
    """

    response = result.final_response

    if not response:
        return """
========== RESPONSE ==========

No response generated.
"""

    citations = "\n".join([f"- {item.name}" for item in response.citations])

    confidence = int(response.confidence * 100)

    safety = "PASSED" if result.success else "FAILED"

    return f"""
========== RESPONSE ==========

{response.answer}


Sources:
{citations or "- No sources found"}


Confidence:
{confidence}%


Safety:
{safety}
"""
