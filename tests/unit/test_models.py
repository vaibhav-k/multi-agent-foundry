"""
Tests for shared Pydantic models.
"""

from src.models import (
    AgentRequest,
    AgentResponse,
    AgentType,
    ChatMessage,
    MessageRole,
)


def test_chat_message_creation():

    message = ChatMessage(
        role=MessageRole.USER,
        content="Hello",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello"


def test_agent_request_creation():

    request = AgentRequest(user_query="How do I setup VPN?")

    assert request.user_query == "How do I setup VPN?"
    assert request.conversation_history == []


def test_agent_response_creation():

    response = AgentResponse(
        agent=AgentType.PLANNER,
        response="Planning completed",
    )

    assert response.success is True
    assert response.agent == AgentType.PLANNER
